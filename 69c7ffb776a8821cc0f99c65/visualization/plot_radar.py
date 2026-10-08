#!/usr/bin/env python3
"""Plot model or character accuracy radars (Python 3.9+, matplotlib).

From the Overleaf project directory:
  python visualization/plot_radar.py --kind models --check-only
  python visualization/plot_radar.py --kind models
  python visualization/plot_radar.py --kind characters --data character_accuracy.csv

Model values are read from tab:main_results in main.tex; these are displayed,
rounded accuracies, not a substitute for recomputing results from predictions.
Character data must be a CSV with columns:
  label,Naive-RAG,Mem0,PersonaDB
Each value is an accuracy in [0,1]. Empty cells, --, and --- mean unavailable.
Use one row per character, with values pooled over the same declared model set
within each setting, as specified in app:character_accuracy. No character
values are inferred from overall model accuracies or the existing PDF.

By default, only rows with all three settings are plotted. --include-partial
retains incomplete rows with gaps, never converting unavailable results to 0.
Generated PDFs use *_generated.pdf names to preserve the manuscript figures.
Caches and output default to the project directory; no packages are installed.
The script recreates the analysis, not the exact styling of the original PDFs.
"""
import argparse
import csv
import math
import os
from pathlib import Path
import re

SETTINGS = ('Naive-RAG', 'Mem0', 'PersonaDB')
COLORS = ('#2166ac', '#d95f02', '#1b9e77')
PROJECT = Path(__file__).resolve().parents[1]


def accuracy(cell):
    cell = cell.strip()
    if cell in ('', '--', '---', '—'):
        return None
    cell = re.sub(r'\\(?:textbf|mathbf)\{([^{}]+)\}', r'\1', cell)
    value = float(cell)
    if not math.isfinite(value) or not 0 <= value <= 1:
        raise ValueError('Accuracy must be finite and in [0,1]: ' + cell)
    return value


def read_models(paper):
    text = paper.read_text(encoding='utf-8')
    table = text.split(r'\label{tab:main_results}', 1)[1].split(r'\end{table*}', 1)[0]
    rows = []
    for line in table.splitlines():
        line = line.strip()
        if not line.startswith(r'\quad '):
            continue
        cells = line.removesuffix(r'\\').split('&')
        if len(cells) != 6:
            raise ValueError('Expected six columns in main-results row: ' + line)
        rows.append((cells[0].removeprefix(r'\quad ').strip(),
                     [accuracy(cell) for cell in cells[2:5]]))
    return rows


def read_characters(path):
    with path.open(encoding='utf-8-sig', newline='') as handle:
        reader = csv.DictReader(handle)
        required = {'label', *SETTINGS}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError('Character CSV requires label,Naive-RAG,Mem0,PersonaDB')
        return [(r['label'].strip(), [accuracy(r[key]) for key in SETTINGS])
                for r in reader]


def select_rows(rows, include_partial=False):
    labels = [label for label, _ in rows]
    if any(not label for label in labels) or len(labels) != len(set(labels)):
        raise ValueError('Labels must be nonempty and unique')
    selected, skipped = [], []
    for label, values in rows:
        if len(values) != 3:
            raise ValueError('Expected three setting values for ' + label)
        usable = any(v is not None for v in values) if include_partial else all(v is not None for v in values)
        (selected if usable else skipped).append((label, values))
    if len(selected) < 3:
        raise ValueError('At least three eligible rows are needed for a radar')
    return selected, skipped


def draw(rows, output, kind, maximum, cache):
    cache.mkdir(parents=True, exist_ok=True)
    os.environ['MPLCONFIGDIR'] = str(cache / 'matplotlib')
    os.environ['XDG_CACHE_HOME'] = str(cache)
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise SystemExit('Plotting requires matplotlib in an existing environment. '
                         'No installation was attempted; --check-only needs only Python.') from exc
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10,
                         'pdf.fonttype': 42, 'axes.unicode_minus': False})
    angles = [2 * math.pi * i / len(rows) for i in range(len(rows))]
    fig, ax = plt.subplots(figsize=(10, 9), subplot_kw={'projection': 'polar'})
    ax.set_theta_offset(math.pi / 2)
    ax.set_theta_direction(-1)
    for j, (name, color) in enumerate(zip(SETTINGS, COLORS)):
        values = [row[1][j] * 100 if row[1][j] is not None else float('nan') for row in rows]
        if not any(math.isfinite(v) for v in values):
            continue
        ax.plot(angles + angles[:1], values + values[:1], color=color,
                linewidth=1.8, marker='o', markersize=4, label=name)
        if all(math.isfinite(v) for v in values):
            ax.fill(angles + angles[:1], values + values[:1], color=color, alpha=0.06)
    ax.set_xticks(angles)
    ax.set_xticklabels([label for label, _ in rows])
    ax.tick_params(axis='x', pad=15)
    ax.set_ylim(0, maximum)
    ticks = [maximum * i / 4 for i in range(1, 5)]
    ax.set_yticks(ticks)
    ax.set_yticklabels([f'{v:g}%' for v in ticks], color='#666666', fontsize=9)
    ax.grid(alpha=0.35)
    ax.set_title(f'Accuracy by {"model" if kind == "models" else "character"}', pad=34)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol=3, frameon=False)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, bbox_inches='tight', pad_inches=0.3)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--kind', choices=['models', 'characters'], default='models')
    parser.add_argument('--paper', type=Path, default=PROJECT / 'main.tex')
    parser.add_argument('--data', type=Path, help='Character accuracy CSV, required for --kind characters')
    parser.add_argument('--output', type=Path)
    parser.add_argument('--cache-dir', type=Path, default=PROJECT / '.plot-cache')
    parser.add_argument('--include-partial', action='store_true')
    parser.add_argument('--max-percent', type=float, default=100)
    parser.add_argument('--check-only', action='store_true')
    args = parser.parse_args()
    if not math.isfinite(args.max_percent) or not 0 < args.max_percent <= 100:
        parser.error('--max-percent must be in (0,100]')
    if args.kind == 'characters' and args.data is None:
        parser.error('--kind characters requires --data')
    rows = read_models(args.paper) if args.kind == 'models' else read_characters(args.data)
    selected, skipped = select_rows(rows, args.include_partial)
    if any(v * 100 > args.max_percent for _, values in selected for v in values if v is not None):
        parser.error('--max-percent would clip an observed accuracy')
    print(f'Loaded {len(rows)} rows; plotting {len(selected)}; skipped {len(skipped)}.')
    if skipped:
        print('Pending/incomplete: ' + ', '.join(label for label, _ in skipped))
    if args.check_only:
        return
    output = args.output or PROJECT / 'figures' / ('radar_3configs_generated.pdf' if args.kind == 'models' else 'per_character_radar_generated.pdf')
    draw(selected, output, args.kind, args.max_percent, args.cache_dir)
    print(output)


if __name__ == '__main__':
    main()
