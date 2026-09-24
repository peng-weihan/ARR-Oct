"""Read-only paper checks; writes audit evidence beside this script. No model calls."""
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TEX = ROOT / 'arr-Oct/69c7ffb776a8821cc0f99c65/main.tex'
SOURCE = ROOT / 'agent-personality-benchmark'
MANIFEST = ROOT / 'nips/rebuttal_experiments/experiment_03_statistical_reanalysis/table3_manifest.json'
ABLATION = ROOT / 'nips/rebuttal_experiments/experiment_04_counterfactual_memory/outputs/formal'


def read_json(path):
    return json.loads(path.read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def choice(value):
    return str(value or '').strip().upper()


def correct(row):
    return bool(row.get('ok')) and choice(row.get('predicted')) in 'ABCD' and len(choice(row.get('predicted'))) == 1 and choice(row.get('predicted')) == choice(row.get('correct_answer'))


def rows_at(path):
    data = read_json(path)
    rows = data['predictions'] if isinstance(data, dict) else data
    index = {row['question_id']: row for row in rows}
    assert len(index) == len(rows), path
    return index


manifest = read_json(MANIFEST)
cells, inputs, errors = {}, [], []
reference = None
for method, template in manifest['methods'].items():
    for model in manifest['models']:
        path = SOURCE / template.format(model=model)
        index = rows_at(path)
        assert len(index) == 673, path
        if reference is None:
            reference = index
        assert set(index) == set(reference), path
        for qid, row in index.items():
            assert all(row.get(k) == reference[qid].get(k) for k in ['correct_answer', 'character_id', 'scenario_id']), (path, qid)
        cells[method, model] = index
        inputs.append({'path': str(path.relative_to(ROOT)), 'sha256': digest(path), 'correct': sum(map(correct, index.values())), 'n': len(index)})

failed = sorted(qid for qid in reference if all(not correct(cells[method, model][qid]) for method in manifest['interactive_methods'] for model in manifest['models']))
converged = [qid for qid in failed if max(Counter(choice(cells['naive_rag', model][qid].get('predicted')) for model in manifest['models'] if choice(cells['naive_rag', model][qid].get('predicted')) in {'A','B','C','D'}).values(), default=0) >= 6]

text = TEX.read_text()
section = text[text.index('DeepSeek-V3.2       & 43.2'):text.index('\\textbf{Mean}       & \\textbf{39.9}')]
paper_ablation = []
for line in section.splitlines():
    if '&' not in line:
        continue
    columns = line.split('&')
    values = [float(x.strip()) for x in columns[1:5]]
    paper_ablation.append({'model': columns[0].strip(), 'values': dict(zip(['C0','C1','C2','C3'], values))})
incompatible = []
for row in paper_ablation:
    for condition, value in row['values'].items():
        if not any(abs(100 * k / 176 - value) <= .050000001 for k in range(177)):
            nearest = round(value * 176 / 100)
            incompatible.append({'model': row['model'], 'condition': condition, 'paper_percent': value, 'nearest_correct': nearest, 'nearest_percent': 100 * nearest / 176})

conditions = ['correct_character_correct_scenario', 'same_character_wrong_scenario', 'wrong_character_same_scenario', 'random_memory']
ablation = []
for model in manifest['models']:
    c0 = None
    for short, condition in zip(['C0','C1','C2','C3'], conditions):
        path = ABLATION / condition / model / 'predictions_top30.json'
        item = {'model': model, 'condition': short, 'path': str(path.relative_to(ROOT)), 'exists': path.exists()}
        if path.exists():
            rows = rows_at(path)
            if short == 'C0':
                c0 = rows
            item.update(n=len(rows), correct=sum(map(correct, rows.values())), sha256=digest(path))
            item['percent'] = 100 * item['correct'] / item['n']
            item['aligned_to_local_C0'] = c0 is not None and set(rows) == set(c0) and all(rows[qid].get('correct_answer') == c0[qid].get('correct_answer') for qid in rows)
        ablation.append(item)

evidence = {
    'scope': 'Local files only. Local predictions are not assumed to be the final submission run; author must establish provenance.',
    'paper_sha256': digest(TEX),
    'manifest_sha256': digest(MANIFEST),
    'main_inputs': inputs,
    'persistent_failure': {'definition': 'All 12 models wrong in each of 3 memory settings', 'count': len(failed), 'question_ids': failed, 'naive_rag_converged_at_least_6': len(converged), 'convergence_percent': 100 * len(converged) / len(failed)},
    'paper_ablation': paper_ablation,
    'incompatible_with_single_run_n176': incompatible,
    'local_ablation': ablation,
    'audit_reliability': {'assumptions': 'Same complete 176x3 nominal rating matrix; standard Fleiss kappa and nominal Krippendorff alpha', 'relation': 'alpha = 1 - (528-1)/528 * (1-kappa)', 'if_kappa_exactly_0_81_alpha': 1-527/528*(1-.81)},
}
(HERE / 'evidence.json').write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'main_cells': len(inputs), 'persistent_failure': evidence['persistent_failure']['count'], 'convergence': evidence['persistent_failure']['convergence_percent'], 'ablation_incompatible_cells': len(incompatible), 'local_ablation_files': sum(x['exists'] for x in ablation), 'source_unchanged_sha256': digest(TEX)}, indent=2))
