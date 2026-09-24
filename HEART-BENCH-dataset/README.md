---
license: cc-by-nc-4.0
language:
- en
task_categories:
- multiple-choice
- text-generation
pretty_name: HEART-BENCH
size_categories:
- 1K<n<10K
configs:
- config_name: scenarios
  data_files:
  - split: train
    path: data/scenarios.parquet
- config_name: mcq
  data_files:
  - split: train
    path: data/mcq.parquet
- config_name: ground_truth
  data_files:
  - split: train
    path: data/ground_truth.parquet
- config_name: characters
  data_files:
  - split: train
    path: data/characters.parquet
---

# HEART-BENCH

A benchmark for evaluating human-like decision making across the lifespan, built around 11 characters with orthogonal Big Five profiles, 64 life-stage scenarios, and 673 ground-truth (character, scenario) pairs with corresponding multiple-choice questions.

## Configs

| Config | Rows | Description |
|---|---|---|
| `characters` | 11 | Character profiles with Big Five traits, self-value logic, core behavioral patterns, and 1,000 episodic memories each (~11,000 memories total). |
| `scenarios` | 64 | Life-stage scenarios across 8 developmental stages (school age → entering midlife), 8 per stage. |
| `ground_truth` | 673 | (character, scenario) pairs with annotated inner consciousness and final decision. |
| `mcq` | 673 | Multiple-choice questions derived from the ground truth, with distractors drawn from other characters' decisions. |

## Loading

```python
from datasets import load_dataset

characters   = load_dataset("HEART-BENCH/HEART-BENCH", "characters",   split="train")
scenarios    = load_dataset("HEART-BENCH/HEART-BENCH", "scenarios",    split="train")
ground_truth = load_dataset("HEART-BENCH/HEART-BENCH", "ground_truth", split="train")
mcq          = load_dataset("HEART-BENCH/HEART-BENCH", "mcq",          split="train")
```

## Schemas

### `characters`
- `id`, `name`, `occupation` (str)
- `big_five` (struct): `openness`, `conscientiousness`, `extraversion`, `agreeableness`, `neuroticism` (float)
- `description`, `self_value_logic` (str)
- `core_patterns` (list of str)
- `episodic_memory_set` (list of structs), each memory:
  - `id`, `timeline`, `context`, `content_summary`, `content_full` (str)
  - `psych_conclusion`, `behavior_policy` (str)
  - `emotion_signature` (struct): `primary`, `secondary` (str), `intensity` (float)
  - `triggers`, `relevance_tags` (list of str)

### `scenarios`
- `id` (str), `stage` (str), `age_range` (str), `age` (int)
- `name`, `category`, `intensity` (str)
- `description_for_agent`, `context_text`, `trigger_event` (str)
- `setting` (struct).

### `ground_truth`
- `character_id`, `scenario_id`, `stage` (str)
- `inner_consciousness` (struct): `summary`, `core_reasoning`, `emotional_tone`, `value_orientation`
- `final_decision` (str)

### `mcq`
- `question_id`, `character_id`, `scenario_id`, `stage`, `correct_answer` (str)
- `options` (list of structs): `label`, `content`, `is_correct`, `is_generated`, `source_character`

## Linking the configs

Each row in `mcq` and `ground_truth` is keyed by (`character_id`, `scenario_id`).
The `characters` config provides per-character profile and memory data joined on `characters.id == ground_truth.character_id == mcq.character_id`.
The `scenarios` config joins on `scenarios.id == ground_truth.scenario_id == mcq.scenario_id`.
