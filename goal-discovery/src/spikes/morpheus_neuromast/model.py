"""Generate the three frozen P6-001 variants without reimplementing M4377."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

CONDITIONS = ("active", "feedback_disabled", "proliferation_disabled")
LOG_INTERVAL = 5_000


@dataclass(frozen=True)
class TransformReport:
    condition: str
    logger_replacements: int
    analysis_blocks_removed: int
    feedback_terms_disabled: int
    probabilities_disabled: int


def _replace_exact(text: str, old: str, new: str, expected: int) -> tuple[str, int]:
    count = text.count(old)
    if count != expected:
        raise ValueError(f"Expected {expected} occurrences of {old!r}, found {count}")
    return text.replace(old, new), count


def _disable_probability(text: str, symbol: str, original: str) -> tuple[str, int]:
    pattern = re.compile(rf'<Variable\b[^>]*\bsymbol="{symbol}"[^>]*/>')
    matches = pattern.findall(text)
    if len(matches) != 1:
        raise ValueError(f"Expected one Variable tag for {symbol!r}, found {len(matches)}")
    tag = matches[0]
    value_count = tag.count(f'value="{original}"')
    if value_count < 1:
        raise ValueError(f"Variable {symbol!r} has no value {original!r}")
    replacement = tag.replace(f'value="{original}"', 'value="0"')
    return text.replace(tag, replacement, 1), 1


def transform_model(source: str, condition: str) -> tuple[str, TransformReport]:
    """Return an instrumented model differing only at frozen XML locations."""

    if condition not in CONDITIONS:
        raise ValueError(f"Unknown condition {condition!r}; choose from {CONDITIONS}")

    transformed, logger_replacements = _replace_exact(
        source,
        '<Logger time-step="1" name="number_cell_vs_time">',
        f'<Logger time-step="{LOG_INTERVAL}" name="number_cell_vs_time">',
        1,
    )

    input_marker = "        <Logger"
    logger_at = transformed.index(input_marker)
    input_at = transformed.index("            <Input>", logger_at) + len("            <Input>")
    observable_symbols = """
                <Symbol symbol-ref="cell.type"/>
                <Symbol symbol-ref="cell.center.x"/>
                <Symbol symbol-ref="cell.center.y"/>
                <Symbol symbol-ref="cell.volume"/>
                <Symbol symbol-ref="HairCell_Neighbours"/>
                <Symbol symbol-ref="Sustentacular_Neighbours"/>
                <Symbol symbol-ref="Mantle_Neighbours"/>"""
    transformed = transformed[:input_at] + observable_symbols + transformed[input_at:]

    transformed, gnuplot_count = re.subn(
        r"\n\s*<Gnuplotter\b.*?</Gnuplotter>", "", transformed, count=1, flags=re.DOTALL
    )
    transformed, graph_count = re.subn(r"\n\s*<ModelGraph\b[^>]*/>", "", transformed, count=1)
    if gnuplot_count != 1 or graph_count != 1:
        raise ValueError(
            "Expected to remove one Gnuplotter and one ModelGraph block, "
            f"removed {gnuplot_count} and {graph_count}"
        )

    feedback_terms_disabled = 0
    probabilities_disabled = 0
    if condition == "feedback_disabled":
        transformed, mantle_count = _replace_exact(
            transformed, "Mantle_Neighbours &lt; umbral", "1 == 1", 1
        )
        transformed, support_count = _replace_exact(
            transformed, "Sustentacular_Neighbours &lt; umbral", "1 == 1", 2
        )
        feedback_terms_disabled = mantle_count + support_count
    elif condition == "proliferation_disabled":
        transformed, pm_count = _disable_probability(transformed, "pm", "0.0001")
        transformed, ps_count = _disable_probability(transformed, "ps", "0.00015")
        probabilities_disabled = pm_count + ps_count

    report = TransformReport(
        condition=condition,
        logger_replacements=logger_replacements,
        analysis_blocks_removed=gnuplot_count + graph_count,
        feedback_terms_disabled=feedback_terms_disabled,
        probabilities_disabled=probabilities_disabled,
    )
    return transformed, report


def write_variants(source: Path, destination: Path) -> dict[str, tuple[Path, TransformReport]]:
    destination.mkdir(parents=True, exist_ok=True)
    source_text = source.read_text(encoding="utf-8")
    variants: dict[str, tuple[Path, TransformReport]] = {}
    for condition in CONDITIONS:
        transformed, report = transform_model(source_text, condition)
        path = destination / f"{condition}.xml"
        path.write_text(transformed, encoding="utf-8")
        variants[condition] = (path, report)
    return variants
