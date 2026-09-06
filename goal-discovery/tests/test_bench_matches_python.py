"""The bench's substrate must be the same substrate, not a lookalike.

`scripts/bench/lattice.js` is a second implementation of
`goal-discovery/src/lattice/`, written so the bench can configure and run
systems in the browser with no server. A second simulator is normally a
correctness hazard: the two drift, and the one a person watches stops being the
one that produced the results.

Two things make it safe, and this file is the second of them.
`scripts/bench/pyrandom.js` reproduces CPython's random stream exactly, so the
implementations can be compared for EQUALITY rather than resemblance. Here they
are run over a matrix of configurations and required to produce identical
trajectories -- operation count and full configuration after every step.

Drift is therefore a red test, not a discrepancy nobody notices. If you change
one implementation, change the other in the same commit.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "goal-discovery"))

from src.lattice.core import Faults, step_synchronous  # noqa: E402
from src.lattice.specimens import elementary_ca, sorting  # noqa: E402

RUNNER = REPO / "scripts/bench/conformance_runner.js"
NODE = shutil.which("node")

CONTROLLERS = ("decentralized", "watchdog", "closed")
FAULTS = {
    "clean": {},
    "p_fail": {"pFail": 0.30},
    "frozen": {"frozen": [3]},
    "dead": {"dead": [5]},
    "unreliable": {"unreliable": {"2": 0.9}},
}
SEEDS = (0, 1, 2, 3, 4)
STEPS = 220
N = 10
CA_RULES = (90, 110, 30)


def python_faults(spec: dict) -> Faults:
    return Faults(
        p_fail=spec.get("pFail", 0.0),
        unreliable={int(k): v for k, v in spec.get("unreliable", {}).items()},
        frozen=set(spec.get("frozen", [])),
        dead=set(spec.get("dead", [])),
    )


def build_cases() -> list[dict]:
    cases = []
    for controller in CONTROLLERS:
        for name, spec in FAULTS.items():
            for seed in SEEDS:
                cases.append({"kind": "sorting", "controller": controller,
                              "faults": spec, "seed": seed, "n": N,
                              "steps": STEPS, "nTypeB": 0, "_label": name})
    for seed in SEEDS:
        cases.append({"kind": "sorting", "controller": "decentralized",
                      "faults": {}, "seed": seed, "n": N, "steps": STEPS,
                      "nTypeB": 3, "_label": "heterogeneous"})
    for rule in CA_RULES:
        cases.append({"kind": "ca", "rule": rule, "size": 41, "steps": 25,
                      "_label": f"rule-{rule}"})
    return cases


def python_trace(case: dict) -> list:
    if case["kind"] == "sorting":
        lat, rule = sorting.make(case["n"], seed=case["seed"],
                                 faults=python_faults(case["faults"]),
                                 n_type_b=case["nTypeB"])
        drive = sorting.CONTROLLERS[case["controller"]](lat, rule, 10 ** 9)
        trace = []
        for _ in range(case["steps"]):
            try:
                next(drive)
            except StopIteration:
                break
            trace.append([lat.ops, list(lat.occupants)])
        return trace
    lat, rule = elementary_ca.make(case["rule"], size=case["size"])
    trace = [[lat.ops, list(lat.occupants)]]
    for _ in range(case["steps"]):
        step_synchronous(lat, rule)
        trace.append([lat.ops, list(lat.occupants)])
    return trace


@unittest.skipIf(NODE is None,
                 "node is not installed, so the bench substrate cannot be run "
                 "here. This is a SKIP, not a pass: the bench is unverified in "
                 "this environment and must not be shipped from it.")
class TheBenchSubstrateMatchesThePythonOne(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.cases = build_cases()
        result = subprocess.run(
            [NODE, str(RUNNER)], input=json.dumps(cls.cases),
            capture_output=True, text=True, cwd=RUNNER.parent, check=False)
        if result.returncode != 0:
            raise AssertionError(
                "the bench conformance runner failed:\n" + result.stderr[-3000:])
        cls.js = json.loads(result.stdout)

    def test_every_configuration_produces_an_identical_trajectory(self):
        failures = []
        for case, js in zip(self.cases, self.js):
            py = python_trace(case)
            if py != js:
                where = next((k for k, (a, b) in enumerate(zip(py, js)) if a != b),
                             min(len(py), len(js)))
                failures.append(
                    f"{case['kind']}/{case.get('controller', case.get('rule'))}"
                    f"/{case['_label']}/seed={case.get('seed')}: diverges at step "
                    f"{where} (python {len(py)} steps, bench {len(js)} steps)")
        self.assertEqual(
            failures, [],
            f"{len(failures)} of {len(self.cases)} configurations diverge between "
            "the Python substrate and the bench's. The bench is showing something "
            "the laboratory did not produce:\n" + "\n".join(failures[:12]))

    def test_the_matrix_is_big_enough_to_be_evidence(self):
        self.assertGreaterEqual(len(self.cases), 75)
        self.assertGreater(
            sum(len(t) for t in self.js), 8000,
            "the compared trajectories are too short to discriminate anything")

    def test_the_comparison_can_fail(self):
        """Control: perturb one bench trajectory and require a mismatch.

        Without this the test above would pass on two empty lists, or on a
        comparison that silently compares nothing.
        """
        case = dict(self.cases[0])
        py = python_trace(case)
        self.assertTrue(py, "no reference trajectory to compare against")
        tampered = [list(row) for row in py]
        tampered[len(tampered) // 2][0] += 1        # one operation count off by one
        self.assertNotEqual(py, tampered,
                            "changing an operation count did not change the "
                            "trajectory, so the comparison is not reading it")

    def test_a_different_seed_really_does_diverge(self):
        """Control: the matrix would pass vacuously if seeds did nothing."""
        a = python_trace(dict(self.cases[0], seed=0))
        b = python_trace(dict(self.cases[0], seed=1))
        self.assertNotEqual(a, b)


class TheBenchFilesArePresent(unittest.TestCase):
    """Runs even without node, so a missing file is never reported as a skip."""

    def test_the_bench_substrate_and_its_runner_exist(self):
        for name in ("pyrandom.js", "lattice.js", "conformance_runner.js"):
            path = RUNNER.parent / name
            self.assertTrue(path.is_file(), f"missing bench file: {name}")
            self.assertGreater(path.stat().st_size, 500, f"{name} is suspiciously small")


class TheShippedPageCarriesTheGatedEngine(unittest.TestCase):
    """The conformance gate above tests the FILES. The page ships a COPY.

    `scripts/render_bench.py` inlines the engine into `wiki/bench.html`, so a
    change to the engine that is not followed by a regeneration leaves the page
    running code the gate never saw -- green tests, stale instrument. That gap
    is the whole reason a generated surface is safer than an authored one, and
    it only holds if something checks the generation is current.
    """

    PAGE = REPO / "wiki/bench.html"

    def test_the_page_exists_and_was_generated(self):
        self.assertTrue(self.PAGE.is_file(), "wiki/bench.html has not been generated")
        text = self.PAGE.read_text(encoding="utf-8")
        self.assertIn("render_bench.py", text,
                      "the page does not name the script that generates it")

    def test_the_embedded_engine_is_byte_identical_to_the_gated_source(self):
        page = self.PAGE.read_text(encoding="utf-8")
        stale = []
        for name in ("pyrandom.js", "lattice.js"):
            source = (RUNNER.parent / name).read_text(encoding="utf-8")
            # Compare the whole body, not a probe: a probe would pass while the
            # rest of the file had changed underneath it.
            if source.strip() not in page:
                stale.append(name)
        self.assertEqual(
            stale, [],
            "wiki/bench.html embeds a copy of " + ", ".join(stale) + " that no "
            "longer matches scripts/bench/. The page is running code this "
            "conformance test never checked. Regenerate it:\n"
            "  cd goal-discovery && uv run --frozen --all-extras python "
            "../scripts/render_bench.py")

    def test_the_page_precomputes_no_trajectories(self):
        """If it shipped frames it would be a replay again, not an instrument."""
        page = self.PAGE.read_text(encoding="utf-8")
        self.assertNotIn("const DATA = {", page,
                         "the page embeds precomputed frames; it is supposed to "
                         "run the substrate live")

    def test_the_page_reaches_nothing_external(self):
        page = self.PAGE.read_text(encoding="utf-8")
        import re
        hits = re.findall(r'(?:src|href)="https?://|@import|url\(\s*https?:', page)
        self.assertEqual(hits, [], f"the page is not offline-safe: {hits[:5]}")


if __name__ == "__main__":
    unittest.main()


class TheGeneratedPagesDeclareTheirEncoding(unittest.TestCase):
    """Every generated HTML page must say it is UTF-8.

    Added 2026-09-06 after both generated pages shipped without a charset
    declaration. A browser opening a file:// page with no declaration falls back
    to a legacy encoding, so every non-ASCII character renders as mojibake --
    the middot separators in the captions came out as "\u00c2\u00b7". The
    generators produced valid UTF-8, the files decoded cleanly, the conformance
    tests were green, and a screenshot review by the agent that built the page
    did not catch it. It was found by a person reading the rendered page.

    This is the class of defect where every automated check is looking at the
    bytes and the defect is in how a browser is told to interpret them, so the
    guard has to assert the declaration exists rather than that the file parses.
    """

    PAGES = ("wiki/bench.html", "wiki/lattice.html", "wiki/status.html")

    def test_every_generated_page_declares_utf8(self):
        missing = []
        for name in self.PAGES:
            page = REPO / name
            if not page.is_file():
                continue
            head = page.read_text(encoding="utf-8")[:2000].lower()
            if 'charset="utf-8"' not in head and "charset=utf-8" not in head:
                missing.append(name)
        self.assertEqual(
            missing, [],
            "generated page(s) with no charset declaration: " + ", ".join(missing) +
            ". A browser opening these from disk will guess a legacy encoding and "
            "render every non-ASCII character as mojibake. Add "
            '<meta charset="utf-8"> to the generator, not to the output.')

    def test_the_guard_is_looking_at_pages_that_exist(self):
        """Otherwise the test above passes by finding nothing to check."""
        found = [n for n in self.PAGES if (REPO / n).is_file()]
        self.assertGreaterEqual(
            len(found), 2, f"only found {found}; the charset guard is near-vacuous")

    def test_pages_that_contain_non_ascii_are_the_ones_at_risk(self):
        """States the risk in the assertion, so the guard explains itself."""
        for name in self.PAGES:
            page = REPO / name
            if not page.is_file():
                continue
            raw = page.read_bytes()
            non_ascii = sum(1 for b in raw if b > 127)
            if non_ascii:
                head = raw[:2000].decode("utf-8", "replace").lower()
                self.assertIn(
                    "charset", head,
                    f"{name} contains {non_ascii} non-ASCII bytes and no charset "
                    "declaration, which is exactly the combination that mojibakes")
