"""Standalone desktop entry point for the P9 blind sorting calibration.

Launch from the repository root with:

    uv run --extra visual-workbench panel serve \
        src/experiments/sorting/lab_app.py --show --port 5012
"""

from __future__ import annotations

import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

import panel as pn

from src.experiments.sorting.laboratory import LAB_CSS, build_sorting_laboratory

pn.extension("tabulator", sizing_mode="stretch_width")


def build_app() -> pn.template.FastListTemplate:
    return pn.template.FastListTemplate(
        title="Goal Discovery · Sorting Laboratory",
        accent_base_color="#f97316",
        header_background="#111827",
        raw_css=[LAB_CSS],
        main=[build_sorting_laboratory()],
        main_layout=None,
        collapsed_sidebar=True,
    )


dashboard = build_app()
dashboard.servable()


if __name__ == "__main__":
    pn.serve(dashboard, port=5012, show=True)
