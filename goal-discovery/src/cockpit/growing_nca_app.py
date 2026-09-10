"""Standalone Panel entrypoint for the frozen Growing NCA evidence workbench.

Run from ``goal-discovery`` with:
    panel serve src/cockpit/growing_nca_app.py --show --port 5011
"""
from __future__ import annotations

import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

import panel as pn

from src.cockpit.growing_nca import NCA_CSS, build_growing_nca_evidence

pn.extension("tabulator", sizing_mode="stretch_width")

template = pn.template.FastListTemplate(
    title="Collective Competence · Growing NCA Evidence",
    accent_base_color="#d35400",
    header_background="#263238",
    raw_css=[NCA_CSS],
    main=[build_growing_nca_evidence()],
    collapsed_sidebar=True,
)
template.servable()
