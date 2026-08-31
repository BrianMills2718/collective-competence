#!/usr/bin/env python3
"""Fail-closed local handoff verifier, NOT a native /goal interception hook.

Run --help. Evidence uses company-planning EndToEndObservationV1 records plus
a hashed artifact inventory and explicit output-quality/handoff review. The
checker validates those records against the supplied installed schema, reads
every cited artifact, reruns the contract's tests, and inspects the live Linux
Panel process. It cannot authenticate an agent's authored observations.

Exit 0: this contract passed now. Exit 1: incomplete/invalid/unavailable.
Receipts are content-addressed and exclusive-created, never overwritten.
Evidence and transient state belong under .company-planning, not tracked source.
Changing code, dependencies or contract requires new evidence. Invoke again
at handoff: a past pass does not guarantee a server remains alive indefinitely.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen


class GateError(ValueError):
    """Acceptance is incomplete; never translate this into a completion pass."""


def require(condition, message):
    if not condition:
        raise GateError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def timestamp(value, hours):
    try:
        when = datetime.fromisoformat(value.replace("Z", "+00:00"))
        age = (datetime.now(timezone.utc) - when).total_seconds()
    except (AttributeError, TypeError, ValueError) as error:
        raise GateError("missing/invalid timezone-aware timestamp") from error
    require(age >= -60, "evidence is from the future")
    require(age <= hours * 3600, "evidence is stale; rerun the journey")


def within(root, relative):
    require(isinstance(relative, str) and relative, "missing artifact path")
    target = (root / relative).resolve()
    require(
        not Path(relative).is_absolute() and target.is_relative_to(root.resolve()),
        "artifact/path escape outside declared root",
    )
    return target


def verify_artifact(root, ref, inventory):
    require(ref in inventory, f"artifact is not registered: {ref}")
    path = within(root, ref)
    require(path.is_file(), f"artifact missing: {ref}")
    require(path.stat().st_size > 0, f"artifact empty: {ref}")
    require(digest(path) == inventory[ref], f"artifact hash changed: {ref}")
    return path


def validate_evidence(contract, bundle, evidence_root, revision, contract_hash):
    require(bundle.get("revision") == revision, "bundle revision mismatch")
    require(
        bundle.get("contract_sha256") == contract_hash,
        "contract changed since observations",
    )
    inventory = bundle.get("artifacts", {})
    require(isinstance(inventory, dict) and inventory, "missing artifact inventory")
    for ref in inventory:
        verify_artifact(evidence_root, ref, inventory)
    hours = contract["max_evidence_age_hours"]
    observations = bundle.get("observations", [])
    ids = [item["criterion_id"] for item in observations]
    require(len(ids) == len(set(ids)), "duplicate journey observation")
    require(set(ids) == set(contract["journeys"]), "required journey coverage mismatch")
    for item in observations:
        label = item["criterion_id"]
        require(item.get("status") == "pass", f"journey {label} not passed")
        require(
            item.get("source_revision") == revision,
            f"journey {label} revision mismatch",
        )
        timestamp(item.get("observed_at"), hours)
        context = item["execution_context"]
        require(context["target"] == bundle["target"], "observation target mismatch")
        require(context["route"] == bundle["route"], "observation route mismatch")
        verify_artifact(evidence_root, context["configuration_ref"], inventory)
        verify_artifact(evidence_root, context["dependency_set_ref"], inventory)
        surfaces = item.get("surface_observations", [])
        require(
            len({s["surface"] for s in surfaces}) == len(surfaces), "duplicate surface"
        )
        for name in contract["required_surfaces"]:
            found = [
                s
                for s in surfaces
                if s["surface"] == name and s["status"] == "observed"
            ]
            require(len(found) == 1, f"journey {label}: {name} evidence missing")
        for surface in surfaces:
            require(
                surface["status"] == "observed",
                f"surface {surface['surface']} unavailable",
            )
            timestamp(surface.get("inspected_at"), hours)
            verify_artifact(evidence_root, surface["evidence_ref"], inventory)
            require(bool(surface.get("observation", "").strip()), "empty inspection")
        for event in item.get("unexpected_events", []):
            require(
                event["disposition"] in ("expected", "explained"),
                "unresolved event or defect",
            )
            verify_artifact(evidence_root, event["event_ref"], inventory)
        verify_artifact(evidence_root, item["outcome"]["evidence_ref"], inventory)
    review = bundle.get("quality_review", {})
    require(
        review.get("status") == "pass" and review.get("reviewer"),
        "quality review not passed",
    )
    require(review.get("unresolved_defects") == [], "quality defects unresolved")
    timestamp(review.get("inspected_at"), hours)
    answers = review.get("answers", [])
    require(
        [a["question"] for a in answers] == contract["quality_questions"],
        "quality review must answer every contracted question",
    )
    for answer in answers:
        require(
            bool(answer.get("assessment", "").strip()), "quality assessment is empty"
        )
        verify_artifact(evidence_root, answer["evidence_ref"], inventory)
    handoff = bundle.get("handoff", {})
    require(handoff.get("fresh_session") is True, "fresh-session handoff missing")
    require(handoff.get("launcher_exited") is True, "launcher exit not observed")
    timestamp(handoff.get("observed_at"), hours)
    verify_artifact(evidence_root, handoff["evidence_ref"], inventory)


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()


def verify_checkout(root, revision):
    require(
        re.fullmatch(r"[0-9a-f]{40}", revision) is not None,
        "expected full commit revision",
    )
    require(git(root, "rev-parse", "HEAD") == revision, "checkout revision mismatch")
    require(
        not git(root, "diff", "HEAD", "--name-only"), "tracked working tree is dirty"
    )
    untracked = git(root, "ls-files", "--others", "--exclude-standard").splitlines()
    require(
        all(p.startswith(".company-planning/") for p in untracked),
        "untracked source files present",
    )


def process_start(pid):
    # stat field 22, accounting for spaces/parentheses in the comm field.
    return (Path("/proc") / str(pid) / "stat").read_text().rsplit(")", 1)[1].split()[19]


def verify_runtime(root, contract, runtime):
    require(
        sys.platform == "linux", "live runtime identity currently requires Linux/WSL"
    )
    pid, port = int(runtime["pid"]), int(runtime["port"])
    require(pid > 0 and 1024 <= port <= 65535, "invalid runtime PID/port")
    proc = Path("/proc") / str(pid)
    require(
        (proc / "cwd").resolve() == within(root, contract["relative_cwd"]),
        "live server checkout mismatch or process missing",
    )
    require(process_start(pid) == runtime["start_ticks"], "server PID reused/restarted")
    command = (proc / "cmdline").read_bytes().replace(b"\0", b" ").decode()
    require("panel" in command and "serve" in command, "runtime is not Panel serve")
    inodes = set()
    for name in ("tcp", "tcp6"):
        for line in (proc / "net" / name).read_text().splitlines()[1:]:
            fields = line.split()
            if int(fields[1].split(":")[-1], 16) == port and fields[3] == "0A":
                inodes.add(f"socket:[{fields[9]}]")
    owned = set()
    for fd in (proc / "fd").iterdir():
        try:
            owned.add(os.readlink(fd))
        except FileNotFoundError:
            pass  # a socket may close while iterating
    require(bool(inodes & owned), "declared server does not own listening port")
    route = contract["route"]
    require(route.startswith("/") and "?" not in route, "invalid app route")
    url = f"http://127.0.0.1:{port}{route}"
    with urlopen(url, timeout=10) as response:
        require(response.status == 200, "app endpoint unavailable")
        require(
            b"bokeh" in response.read().lower(), "endpoint is not a Bokeh application"
        )
    return {"pid": pid, "port": port, "start_ticks": runtime["start_ticks"], "url": url}


def execute_tests(contract, root, python, output):
    results = []
    tests = contract["mandatory_tests"]
    require(
        tests and len({t["id"] for t in tests}) == len(tests),
        "missing/duplicate mandatory tests",
    )
    for test in tests:
        require(re.fullmatch(r"[a-z0-9-]+", test["id"]), "invalid test id")
        command = [s.replace("{python}", python) for s in test["argv"]]
        result = subprocess.run(
            command,
            cwd=within(root, test["cwd"]),
            capture_output=True,
            text=True,
            timeout=300,
            check=False,
        )
        log = output / f"{test['id']}.log"
        log.write_text(result.stdout + result.stderr)
        require(
            result.returncode == 0, f"mandatory test failed: {test['id']} (see {log})"
        )
        require(
            not re.search(r"Ran 0 tests|no tests ran", result.stdout + result.stderr),
            f"mandatory test collection empty: {test['id']}",
        )
        require(
            not re.search(
                r"\b[1-9][0-9]* skipped\b|skipped=[1-9]", result.stdout + result.stderr
            ),
            f"mandatory tests skipped: {test['id']}; classify explicitly, do not waive silently",
        )
        results.append(
            {
                "id": test["id"],
                "argv": command,
                "exit_code": 0,
                "log": str(log),
                "sha256": digest(log),
            }
        )
    return results


def launch(root, revision, python, port):
    """Start only our separate preview, surviving the launcher; never stop another server."""
    verify_checkout(root, revision)
    directory = root / ".company-planning" / "launches"
    directory.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    log = directory / f"{stamp}.log"
    with log.open("xb") as stream:
        child = subprocess.Popen(
            [
                str(Path(python).absolute()),
                "-m",
                "panel",
                "serve",
                "src/cockpit/app.py",
                "--address",
                "127.0.0.1",
                "--port",
                str(port),
                "--allow-websocket-origin",
                f"localhost:{port}",
                "--allow-websocket-origin",
                f"127.0.0.1:{port}",
            ],
            cwd=root / "goal-discovery",
            stdin=subprocess.DEVNULL,
            stdout=stream,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
    runtime = {"pid": child.pid, "port": port, "start_ticks": process_start(child.pid)}
    try:
        for attempt in range(40):
            require(child.poll() is None, f"preview exited; see {log}")
            try:
                verify_runtime(
                    root, {"relative_cwd": "goal-discovery", "route": "/app"}, runtime
                )
                break
            except (GateError, OSError):
                if attempt == 39:
                    raise
                time.sleep(0.25)
        verify_checkout(root, revision)
        record = {
            "record_type": "completion_preview_launch",
            "revision": revision,
            "target": str(root / "goal-discovery"),
            "runtime": runtime,
            "python": str(Path(python).absolute()),
            "dependency_lock_sha256": digest(root / "goal-discovery/uv.lock"),
            "log": str(log),
            "started_at": datetime.now(timezone.utc).isoformat(),
        }
        path = directory / f"{stamp}.json"
        with path.open("x") as stream:
            json.dump(record, stream, indent=2)
        return {"launch_ref": str(path), **record}
    except Exception:
        child.terminate()  # Only the exact child created by this call.
        child.wait(timeout=10)
        raise


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    parser.add_argument(
        "--revision", required=True, help="Exact expected clean source commit"
    )
    parser.add_argument(
        "--evidence",
        type=Path,
        help="Bundle JSON with hashed artifact inventory",
    )
    parser.add_argument(
        "--observation-schema",
        type=Path,
        help="Installed company-planning contracts/end-to-end-observation.schema.json",
    )
    parser.add_argument(
        "--python",
        default=sys.executable,
        help="Interpreter with project's locked test extras",
    )
    parser.add_argument(
        "--launch",
        action="store_true",
        help="Launch an independent revision-bound preview, not a completion check",
    )
    parser.add_argument("--port", type=int, default=5013)
    args = parser.parse_args(argv)
    try:
        root = args.root.resolve()
        if args.launch:
            print(json.dumps(launch(root, args.revision, args.python, args.port)))
            return 0
        require(
            args.evidence is not None and args.observation_schema is not None,
            "verification requires --evidence and --observation-schema",
        )
        import jsonschema

        contract_path = root / "scripts/completion_contract.json"
        contract = json.loads(contract_path.read_text())
        contract_hash = digest(contract_path)
        verify_checkout(root, args.revision)
        bundle = json.loads(args.evidence.read_text())
        bundle_hash = digest(args.evidence)
        schema = json.loads(args.observation_schema.read_text())
        schema_hash = digest(args.observation_schema)
        require(
            schema.get("title") == "EndToEndObservationV1", "wrong observation schema"
        )
        validator = jsonschema.Draft202012Validator(
            schema, format_checker=jsonschema.FormatChecker()
        )
        for observation in bundle["observations"]:
            validator.validate(observation)
        validate_evidence(
            contract,
            bundle,
            args.evidence.parent.resolve(),
            args.revision,
            digest(contract_path),
        )
        runtime = verify_runtime(root, contract["runtime"], bundle["runtime"])
        require(
            bundle["target"] == str(root / contract["runtime"]["relative_cwd"]),
            "bundle target mismatch",
        )
        require(bundle["route"] == runtime["url"], "bundle route mismatch")
        launch_record = json.loads(
            verify_artifact(
                args.evidence.parent.resolve(),
                bundle["launch_ref"],
                bundle["artifacts"],
            ).read_text()
        )
        require(
            launch_record["revision"] == args.revision,
            "server launched at another revision",
        )
        require(
            launch_record["runtime"] == bundle["runtime"],
            "server differs from launch record",
        )
        require(launch_record["target"] == bundle["target"], "launch checkout mismatch")
        require(
            launch_record["dependency_lock_sha256"]
            == digest(root / "goal-discovery/uv.lock"),
            "launch dependency lock mismatch",
        )
        output = (
            root
            / ".company-planning"
            / "verification"
            / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        )
        output.mkdir(parents=True, exist_ok=False)
        results = execute_tests(contract, root, args.python, output)
        require(
            digest(contract_path) == contract_hash,
            "contract mutated during verification",
        )
        require(
            digest(args.evidence) == bundle_hash,
            "evidence bundle mutated during verification",
        )
        require(
            digest(args.observation_schema) == schema_hash,
            "schema mutated during verification",
        )
        # Catch source changes or a dying/replaced server during the test run.
        verify_checkout(root, args.revision)
        verify_runtime(root, contract["runtime"], bundle["runtime"])
        validate_evidence(
            contract,
            bundle,
            args.evidence.parent.resolve(),
            args.revision,
            digest(contract_path),
        )
        receipt = {
            "schema_version": "1.0",
            "verifier_outcome": "pass",
            "scope": contract["scope"],
            "evidence_revision": args.revision,
            "contract_sha256": digest(contract_path),
            "bundle_sha256": digest(args.evidence),
            "schema_sha256": digest(args.observation_schema),
            "verified_at": datetime.now(timezone.utc).isoformat(),
            "runtime": runtime,
            "tests": results,
            "native_goal_interception": False,
            "limits": contract["limits"],
        }
        encoded = (json.dumps(receipt, indent=2, sort_keys=True) + "\n").encode()
        receipt_hash = hashlib.sha256(encoded).hexdigest()
        path = output / f"pass-{receipt_hash}.json"
        with path.open("xb") as stream:
            stream.write(encoded)
        print(
            json.dumps(
                {
                    "verifier_outcome": "pass",
                    "receipt_ref": str(path),
                    "receipt_sha256": receipt_hash,
                    "evidence_revision": args.revision,
                }
            )
        )
        return 0
    except Exception as error:  # noqa: BLE001 -- process boundary must fail closed, including validator faults
        # Fail closed even if the validator/runtime/dependency itself is broken.
        print(
            json.dumps(
                {
                    "verifier_outcome": "fail",
                    "error": f"{type(error).__name__}: {error}",
                    "completion_allowed": False,
                }
            ),
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
