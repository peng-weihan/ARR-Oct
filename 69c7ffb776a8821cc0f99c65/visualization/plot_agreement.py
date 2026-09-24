import json, os, numpy as np, matplotlib.pyplot as plt, matplotlib

base = "/Users/yuling/Desktop/agentmentalbench/experiments/results/naive_rag"

models_ordered = [
    "gemini-3.1-pro-preview", "gemini-3-flash-preview",
    "claude-sonnet-4-6", "claude-haiku-4-5",
    "gpt-5.4", "gpt-5.4-mini",
    "deepseek-v3.2", "deepseek-v4-flash", "deepseek-v4-pro",
    "qwen3.5-35b-a3b", "qwen3.5-122b-a10b", "qwen3.5-397b-a17b",
]

display_names = [
    "Gemini-3.1-Pro", "Gemini-3-Flash",
    "Sonnet-4.6", "Haiku-4.5",
    "GPT-5.4", "GPT-5.4-mini",
    "DS-V3.2", "DS-V4-Flash", "DS-V4-Pro",
    "Qwen-35B", "Qwen-122B", "Qwen-397B",
]

group_boundaries = [2, 4, 6, 9]  # indices where new family starts

# Load predictions
preds = {}
for m in models_ordered:
    fp = os.path.join(base, m, "predictions_top30.json")
    with open(fp) as f:
        data = json.load(f)["predictions"]
    preds[m] = {d["question_id"]: d["predicted"] for d in data}

# All question ids
all_qids = sorted(preds[models_ordered[0]].keys())
n = len(models_ordered)

# Agreement matrix
agree = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        if i == j:
            agree[i, j] = 1.0
        elif j > i:
            same = sum(1 for q in all_qids if preds[models_ordered[i]].get(q) == preds[models_ordered[j]].get(q))
            agree[i, j] = agree[j, i] = same / len(all_qids)

# Mask diagonal
agree_masked = np.ma.masked_where(np.eye(n, dtype=bool), agree)

# Plot
matplotlib.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "DejaVu Sans"],
    "font.weight": 800,
})

fig, ax = plt.subplots(figsize=(8, 7))
off_diag = agree[np.triu_indices(n, k=1)]
im = ax.imshow(agree_masked, cmap="YlGnBu", vmin=off_diag.min() * 0.95, vmax=off_diag.max() * 1.02)

ax.set_xticks(range(n))
ax.set_yticks(range(n))
ax.set_xticklabels(display_names, rotation=45, ha="right", fontsize=8, fontweight=800)
ax.set_yticklabels(display_names, fontsize=8, fontweight=800)

# Annotate (skip diagonal)
for i in range(n):
    for j in range(n):
        if i == j:
            ax.text(j, i, "—", ha="center", va="center", fontsize=7, color="#999999")
        else:
            color = "white" if agree[i, j] > off_diag.mean() + off_diag.std() else "black"
            ax.text(j, i, f"{agree[i,j]:.2f}", ha="center", va="center", fontsize=8.5, fontweight=800, color=color)

# Group separators
for b in group_boundaries:
    ax.axhline(b - 0.5, color="white", linewidth=2)
    ax.axvline(b - 0.5, color="white", linewidth=2)

cbar = fig.colorbar(im, ax=ax, shrink=0.8)
cbar.set_label("Agreement Rate", fontweight=800, fontsize=10)

# No title (will use LaTeX caption)
plt.tight_layout()

os.makedirs("/Users/yuling/Desktop/agentmentalbench/figures", exist_ok=True)
fig.savefig("/Users/yuling/Desktop/agentmentalbench/figures/model_agreement.pdf", dpi=300, bbox_inches="tight")
print("Saved.")
