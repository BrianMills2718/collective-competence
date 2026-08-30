"""Static figures only. Every figure must be regenerable from saved raw data."""

from __future__ import annotations

from pathlib import Path


def _plt():
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    return plt


def render_array(values: list[int], title: str, path: Path, frozen: list[str] | None = None):
    """One array as a colour strip, with frozen cells marked."""
    plt = _plt()
    fig, ax = plt.subplots(figsize=(max(4.0, len(values) * 0.16), 1.7))
    ax.imshow([values], aspect="auto", cmap="viridis", interpolation="nearest")
    if frozen:
        for i, f in enumerate(frozen):
            if f != "none":
                ax.text(
                    i,
                    0,
                    "x" if f == "moveable" else "X",
                    ha="center",
                    va="center",
                    color="red",
                    fontsize=8,
                    fontweight="bold",
                )
    ax.set_yticks([])
    ax.set_xlabel("position")
    ax.set_title(title, fontsize=10)
    fig.tight_layout()
    fig.savefig(path, dpi=140)
    plt.close(fig)
    return path


def render_recovery(
    series: dict[str, list[float]], x: list[int], branch_x: int, title: str, path: Path
):
    """Representation values against sorting steps, with the branch marked."""
    plt = _plt()
    fig, axes = plt.subplots(len(series), 1, figsize=(8.0, 2.0 * len(series)), sharex=True)
    if len(series) == 1:
        axes = [axes]
    for ax, (name, ys) in zip(axes, series.items()):
        ax.plot(x, ys, lw=1.6)
        ax.axvline(branch_x, color="crimson", ls="--", lw=1.2)
        ax.set_ylabel(name, fontsize=8)
        ax.grid(alpha=0.3)
    axes[-1].set_xlabel("sorting steps (comparisons + swaps)")
    axes[0].set_title(title, fontsize=10)
    fig.tight_layout()
    fig.savefig(path, dpi=140)
    plt.close(fig)
    return path
