"""Audit regressions: a missing output must be retained; invalid evidence abstains."""

import copy
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from src.experiments.probe_selection import run


def test_zero_exit_without_csv_is_explicit_failure(tmp_path, monkeypatch):
    # Real local copying/staging with a fake successful subprocess, no simulator.
    monkeypatch.setenv("P11_NETLOGO_STAGING", "/mnt/c/Users/thela/AppData/Local/Temp")
    if not Path("/mnt/c/Users/thela/AppData/Local/Temp").is_dir():
        pytest.skip("Windows-local staging unavailable")
    monkeypatch.setattr(run, "_command", lambda *a, **kw: ["stub"])
    monkeypatch.setattr(run, "_netlogo_root", lambda: tmp_path)
    monkeypatch.setattr(run.subprocess, "run", lambda *a, **kw: SimpleNamespace(
        returncode=0, stdout="no data", stderr=""))
    with pytest.raises(RuntimeError, match="no observation CSV"):
        run.run_engine(tmp_path, "case-a", None)
    assert (tmp_path / "case-a-prefix.log").read_text() == "no data"
    assert json.loads((tmp_path / "case-a-prefix-staging.json").read_text())["staged_inputs_unchanged"]


def test_failed_nonempty_probe_does_not_display_support(tmp_path):
    pn = pytest.importorskip("panel")
    from src.cockpit.probe_selection import build_probe_selection
    from test_probe_selection_view import evidence_fixture

    evidence_fixture(tmp_path)
    path = tmp_path / "evaluation.json"
    evidence = json.loads(path.read_text())
    for probe in evidence["fixtures"][0]["probes"].values():
        probe["integrity"] = False
    path.write_text(json.dumps(copy.deepcopy(evidence)))
    view = build_probe_selection(tmp_path)
    view[4][1].value = 64
    assert "UNAVAILABLE" in view[6].object
    assert "PASSIVE" not in view[6].object
    assert "support: **unavailable**" in view[8][0].object
    assert isinstance(view, pn.Column)
