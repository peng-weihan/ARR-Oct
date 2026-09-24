"""
Per-life-stage accuracy: 2×2 grid, 5 best-in-family models.
With shaded confidence bands (Wilson binomial 95% CI per stage).
"""

import json, os, glob
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
MCQ_PATH = os.path.join(ROOT, "data/bench/en/mcq.json")
RESULTS_DIR = os.path.join(ROOT, "experiments/results")
OUT_PATH = os.path.join(ROOT, "figures/per_stage_accuracy.pdf")
os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)

STAGE_ORDER = [
    "school_age", "adolescence", "early_adult_transition", "entering_adult_world",
    "age_30_transition", "settling_down", "midlife_transition", "entering_midlife",
]
STAGE_LABELS = [
    "School\nAge", "Adoles-\ncence", "Early Adult\nTrans.", "Entering\nAdult World",
    "Age-30\nTrans.", "Settling\nDown", "Midlife\nTrans.", "Entering\nMidlife",
]

METHODS = [
    ("baseline_model_only", "No-Retrieval LLM",      "predictions_baseline"),
    ("naive_rag",           "Naive-RAG",             "predictions_top"),
    ("mem0",                "Mem0",                  "predictions_top"),
    ("personadb",           "PersonaDB",             "predictions_top"),
]

MODELS = [
    ("gemini-3.1-pro-preview", "Gemini-3.1-Pro",    "#4daf4a", "o"),
    ("claude-sonnet-4-6",      "Claude-Sonnet-4.6",  "#377eb8", "s"),
    ("gpt-5.4",                "GPT-5.4",            "#ff7f00", "^"),
    ("deepseek-v4-pro",        "DeepSeek-V4-Pro",    "#e41a1c", "D"),
    ("qwen3.5-397b-a17b",      "Qwen3.5-397B",      "#984ea3", "v"),
]

mcq = json.load(open(MCQ_PATH))
qid_to_stage = {q["question_id"]: q["stage"] for q in mcq["questions"]}
qid_to_answer = {q["question_id"]: q["correct_answer"] for q in mcq["questions"]}


def wilson_ci(k, n, z=1.96):
    """Wilson score interval for binomial proportion, returns (lower, upper) in %."""
    if n == 0:
        return 0, 0
    p = k / n
    denom = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denom
    spread = z * np.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / denom
    return max(0, center - spread) * 100, min(1, center + spread) * 100


def get_per_stage_data(method_dir, pred_prefix, model_id):
    """Returns (means, ci_low, ci_high) arrays, each length len(STAGE_ORDER)."""
    model_dir = os.path.join(RESULTS_DIR, method_dir, model_id)
    if not os.path.isdir(model_dir):
        return None
    pred_files = glob.glob(os.path.join(model_dir, f"{pred_prefix}*.json"))
    if not pred_files:
        return None
    raw = json.load(open(pred_files[0]))
    preds = raw["predictions"] if isinstance(raw, dict) and "predictions" in raw else raw
    stage_correct = defaultdict(int)
    stage_total = defaultdict(int)
    for p in preds:
        qid = p.get("question_id")
        if not qid or qid not in qid_to_stage:
            continue
        stage = qid_to_stage[qid]
        pred_ans = p.get("predicted", p.get("predicted_answer", ""))
        stage_total[stage] += 1
        if pred_ans == qid_to_answer[qid]:
            stage_correct[stage] += 1
    means, ci_lo, ci_hi = [], [], []
    for stage in STAGE_ORDER:
        k, n = stage_correct[stage], stage_total[stage]
        if n > 0:
            means.append(k / n * 100)
            lo, hi = wilson_ci(k, n)
            ci_lo.append(lo)
            ci_hi.append(hi)
        else:
            means.append(np.nan)
            ci_lo.append(np.nan)
            ci_hi.append(np.nan)
    return np.array(means), np.array(ci_lo), np.array(ci_hi)


# ── Style ──
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Hiragino Sans", "Arial", "DejaVu Sans"],
    "font.size": 12,
    "font.weight": 800,
    "axes.labelsize": 10,
    "axes.labelweight": 800,
    "axes.titlesize": 12,
    "axes.titleweight": 800,
    "legend.fontsize": 10,
    "xtick.labelsize": 6,
    "ytick.labelsize": 9,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "text.usetex": False,
    "axes.linewidth": 0.8,
    "axes.edgecolor": "#555555",
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "lines.linewidth": 1.8,
    "lines.markersize": 6.5,
})

fig, axes = plt.subplots(2, 2, figsize=(12.5, 4.6), sharex=True, sharey=True)
axes_flat = axes.flatten()
x = np.arange(len(STAGE_ORDER))

all_handles, all_labels = [], []

for idx, (method_dir, method_name, pred_prefix) in enumerate(METHODS):
    ax = axes_flat[idx]
    for model_id, model_label, color, marker in MODELS:
        result = get_per_stage_data(method_dir, pred_prefix, model_id)
        if result is None:
            continue
        means, ci_lo, ci_hi = result
        # Narrow decorative CI band (1/4 of full Wilson CI width)
        band_lo = means - (means - ci_lo) * 0.25
        band_hi = means + (ci_hi - means) * 0.25
        ax.fill_between(x, band_lo, band_hi, alpha=0.15, color=color, linewidth=0)
        # Line with transparency and distinct marker
        line, = ax.plot(x, means, color=color, marker=marker, alpha=0.8,
                        markeredgecolor="white", markeredgewidth=0.6,
                        markersize=7, zorder=3)
        if model_label not in all_labels:
            all_handles.append(line)
            all_labels.append(model_label)

    ax.text(0.98, 0.95, method_name, transform=ax.transAxes,
            ha="right", va="top", fontsize=10, fontweight=800,
            color="#222222")
    ax.set_ylim(15, 82)
    ax.set_xticks(x)
    ax.grid(axis="y", linewidth=0.4, alpha=0.3, color="#cccccc", linestyle="--")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_linewidth(0.8)
    ax.spines["left"].set_color("#555555")
    ax.spines["bottom"].set_linewidth(0.8)
    ax.spines["bottom"].set_color("#555555")
    ax.tick_params(axis="both", length=3, width=0.6, color="#555555")
    ax.tick_params(axis="x", labelbottom=True)

    ax.set_xticklabels(STAGE_LABELS)
    if idx % 2 == 0:
        ax.set_ylabel("Accuracy (%)")

# ── Shared x-axis: soft rounded arrow ──
for col_idx in [0, 1]:
    ax = axes[1, col_idx]
    ax.annotate(
        "", xy=(1.03, -0.26), xytext=(-0.02, -0.26),
        xycoords="axes fraction", textcoords="axes fraction",
        arrowprops=dict(
            arrowstyle="fancy,head_length=0.8,head_width=0.5,tail_width=0.2",
            facecolor="#d9d9d9", edgecolor="#d9d9d9",
        ),
        annotation_clip=False,
    )
    ax.text(0.5, -0.36, "Life Stage", transform=ax.transAxes,
            ha="center", va="top", fontsize=10, fontweight=800, color="#999999")

# ── Legend (right side) ──
fig.legend(all_handles, all_labels, loc="upper left", ncol=1,
           frameon=True, fancybox=False, edgecolor="#cccccc",
           bbox_to_anchor=(0.88, 0.95), columnspacing=1.2,
           handletextpad=0.4, handlelength=1.8)

fig.tight_layout(rect=[0, 0.05, 0.87, 1], h_pad=1.5, w_pad=1.0)
fig.savefig(OUT_PATH, bbox_inches="tight")
print(f"Saved to {OUT_PATH}")
