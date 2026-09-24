# Memory Ablation Results

| 模型 | C0：正确角色＋正确场景 | C1：正确角色＋错误场景 | C2：错误角色＋正确场景 | C3 (Random-memory) | C0−C1 (pp) | C0−C2 (pp) | C0−C3 (pp) |
|---|---:|---:|---:|---:|---:|---:|---:|
| DeepSeek-V3.2 | 43.2% | 38.9% | 19.9% | 37.8% | +4.3 | +23.3 | +5.4 |
| DeepSeek-V4-Flash | 34.7% | 30.6% | 24.4% | 30.1% | +4.1 | +10.3 | +4.6 |
| DeepSeek-V4-Pro | 41.5% | 35.9% | 22.2% | 36.8% | +5.6 | +19.3 | +4.7 |
| Qwen3.5-35B-A3B | 32.4% | 30.2% | 20.5% | 29.1% | +2.2 | +11.9 | +3.3 |
| Qwen3.5-122B-A10B | 33.5% | 31.2% | 23.3% | 30.1% | +2.3 | +10.2 | +3.4 |
| Qwen3.5-397B-A17B | 34.7% | 31.9% | 23.3% | 30.9% | +2.8 | +11.4 | +3.8 |
| GPT-5.4-mini | 32.4% | 29.2% | 20.5% | 28.7% | +3.2 | +11.9 | +3.7 |
| GPT-5.4 | 31.8% | 28.1% | 19.3% | 28.8% | +3.7 | +12.5 | +3.0 |
| Claude-Haiku-4.5 | 31.8% | 25.7% | 24.4% | 26.1% | +6.1 | +7.4 | +5.7 |
| Claude-Sonnet-4.6 | 41.5% | 34.7% | 24.4% | 33.8% | +6.8 | +17.1 | +7.7 |
| Gemini-3-Flash | 56.3% | 48.4% | 23.9% | 47.9% | +7.9 | +32.4 | +8.4 |
| Gemini-3.1-Pro | 65.3% | 53.6% | 26.1% | 53.8% | +11.7 | +39.2 | +11.5 |
| **Overall** | **39.9%** | **34.9%** | **22.7%** | **34.5%** | **+5.1** | **+17.2** | **+5.4** |

> Differences are calculated from the displayed one-decimal accuracies and may differ from unrounded estimates by 0.1 percentage points.

## Model-panel statistical analysis

The following paired analysis treats the 12 evaluated LLMs as the statistical units. It is a model-panel analysis based on the aggregate accuracies above; it is not an item-level analysis and therefore does not substitute for scenario-cluster confidence intervals or McNemar tests.

The four conditions differ overall (Friedman $\chi^2(3)=32.80$, $p=3.55\times10^{-7}$). Pairwise effects use two-sided exact sign-flip tests across models, with Holm correction over all six condition pairs. The 95% CIs are paired $t$ intervals over the 12 model-level differences.

| Contrast | Mean difference (pp) | 95% CI (pp) | Models favoring left | Raw $p$ | Holm $p$ |
|---|---:|---:|---:|---:|---:|
| C0 $-$ C1 | +5.06 | [+3.30, +6.82] | 12/12 | 0.00049 | 0.00293 |
| C0 $-$ C2 | +17.24 | [+11.00, +23.48] | 12/12 | 0.00049 | 0.00293 |
| C0 $-$ C3 | +5.43 | [+3.80, +7.06] | 12/12 | 0.00049 | 0.00293 |
| C1 $-$ C2 | +12.18 | [+7.28, +17.08] | 12/12 | 0.00049 | 0.00293 |
| C1 $-$ C3 | +0.38 | [$-$0.09, +0.84] | 8/12 | 0.11475 | 0.11475 |
| C3 $-$ C2 | +11.81 | [+6.88, +16.74] | 12/12 | 0.00049 | 0.00293 |

Across this fixed model panel, C0 consistently outperforms both mismatched and random-memory controls. C1 and C3 are not statistically resolved, while both outperform C2; the nonsignificant C1--C3 contrast does not establish equivalence. The supported partial ordering is therefore $\mathrm{C0} > \{\mathrm{C1},\mathrm{C3}\} > \mathrm{C2}$ at the model-panel level.
