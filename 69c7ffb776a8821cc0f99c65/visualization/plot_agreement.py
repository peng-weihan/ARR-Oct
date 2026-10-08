#!/usr/bin/env python3
"""Regenerate the 16-model Naive-RAG figure from its frozen matrix.

Run: python3 visualization/plot_agreement.py
Requires numpy and matplotlib; makes no model or network calls.
Question-level provenance and the full analysis are in the workspace artifact
outputs/model_agreement_naive_rag_20261008/analysis_summary.json.
"""
import json
import os
import tempfile
from pathlib import Path
import numpy as np

def draw_heatmap(matrix, models, n_min, n_max, out):
    cache = Path(tempfile.gettempdir()) / "codex-model-agreement-plot-cache"
    cache.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MPLCONFIGDIR", str(cache / "matplotlib"))
    os.environ.setdefault("XDG_CACHE_HOME", str(cache))
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import PercentFormatter

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "pdf.fonttype": 42,
                         "ps.fonttype": 42, "svg.fonttype": "none", "axes.unicode_minus": False})
    n = len(models)
    fig, ax = plt.subplots(figsize=(13.8, 12.6), facecolor="white")
    fig.subplots_adjust(left=0.205, right=0.90, bottom=0.235, top=0.87)
    cmap = plt.get_cmap("YlGnBu").copy()
    cmap.set_bad("#f0f2f5")
    masked = np.ma.array(matrix, mask=np.eye(n, dtype=bool))
    im = ax.imshow(masked, cmap=cmap, vmin=0, vmax=100, interpolation="nearest")
    names = [m["label"] for m in models]
    ax.set_xticks(np.arange(n))
    ax.set_yticks(np.arange(n))
    ax.set_xticklabels(names, rotation=48, ha="right", rotation_mode="anchor", fontsize=10)
    ax.set_yticklabels(names, fontsize=10)
    family_colors = {
        "Gemini": "#2166AC",
        "Claude": "#A65318",
        "GPT": "#16734A",
        "DeepSeek": "#7953A2",
        "Qwen": "#B42A50",
    }
    for labels in (ax.get_xticklabels(), ax.get_yticklabels()):
        for label, model in zip(labels, models):
            label.set_color(family_colors[model["family"]])
    ax.tick_params(axis="both", length=0, pad=7)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_xticks(np.arange(-0.5, n, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, n, 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=0.45)
    ax.tick_params(which="minor", bottom=False, left=False)
    for i in range(n):
        for j in range(n):
            if i == j:
                value, color = "—", "#969faa"
            else:
                value = f"{matrix[i, j]:.1f}"
                r, g, b, _ = cmap(matrix[i, j] / 100)
                lum = 0.2126*r + 0.7152*g + 0.0722*b
                color = "white" if lum < 0.53 else "#15202b"
            ax.text(j, i, value, ha="center", va="center", fontsize=9.1, color=color)
    for i in range(1, n):
        if models[i]["family"] != models[i-1]["family"]:
            ax.axhline(i-0.5, color="white", linewidth=2.8)
            ax.axvline(i-0.5, color="white", linewidth=2.8)
    fig.suptitle("Model–Model Agreement Analysis", fontsize=22, fontweight="bold", y=0.958, color="#172b42")
    fig.text(0.5, 0.923, f"Naive-RAG@30  ·  {n} models  ·  673-question dataset", ha="center", fontsize=13, color="#45566a")
    cax = fig.add_axes([0.895, 0.325, 0.017, 0.465])
    colorbar = fig.colorbar(im, cax=cax, ticks=np.arange(0, 101, 20))
    colorbar.ax.yaxis.set_major_formatter(PercentFormatter(xmax=100, decimals=0))
    colorbar.set_label("Same-option agreement", labelpad=10, fontsize=11)
    colorbar.outline.set_visible(False)
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    for text in fig.findobj(matplotlib.text.Text):
        if text.get_visible() and text.get_text():
            bbox = text.get_window_extent(renderer)
            assert bbox.x0 >= 0 and bbox.y0 >= 0 and bbox.x1 <= fig.bbox.width and bbox.y1 <= fig.bbox.height, ("Clipped label", text.get_text())
    for extension in ("pdf",):
        fig.savefig(out / f"model_agreement.{extension}", dpi=300, facecolor="white", bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)

if __name__ == "__main__":
    base = Path(__file__).resolve().parent
    data = json.loads((base / "model_agreement_data.json").read_text())
    output = base.parent / "figures"
    output.mkdir(exist_ok=True)
    draw_heatmap(np.asarray(data["agreement_percent"]), data["models"], *data["pairwise_n_range"], output)
    print(output / "model_agreement.pdf")
