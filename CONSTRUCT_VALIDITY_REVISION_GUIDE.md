# HEART-Bench 构念效度与主张边界修改指南

## 一、核心判断

当前论文将 HEART-Bench 描述为评估 LLM agents 的 **human-like psychology**，但现有实验并未使用真实人物、真实行为或真实人类心理反应作为效标。论文实际测量的是：

> **psychology-informed, memory-grounded persona-consistent action selection in controlled synthetic scenarios**

可使用更简洁的概括：

> **psychology-informed synthetic persona consistency**

这里需要严格区分：

- **psychology-informed** 描述 Big Five、Schwartz、DIAMONDS 等理论对数据构造的指导作用；
- **persona consistency** 描述模型选择与预定义合成人格及专家裁定参考响应的一致程度；
- 现有证据不支持模型具有真实心理、情绪、意识，也不支持模型能够预测真实人类行为。

因此，这不是只修改标题和结论即可解决的措辞问题，而是需要统一修正标题、摘要、研究问题、贡献、方法定义、指标、结果解释、结论、局限性和附录术语的构念效度问题。

## 二、证据与主张边界

| 现有证据 | 可以支持的主张 | 不能支持的主张 |
|---|---|---|
| Big Five、Schwartz、DIAMONDS 指导数据构造 | psychology-informed benchmark design | 模型具有人类心理或真实情绪 |
| 专家评审合成人格的候选响应 | 内容合理性、内部一致性、参考标签可靠性 | 真实人物会采取相同反应 |
| MCQ 与专家参考标签的一致率 | reference-label agreement、persona-consistent action selection | human-like psychology 或真实心理能力 |
| 记忆内容与归属消融 | 模型决策会受到编码的人格和记忆信息影响 | 人类记忆—行为机制或心理因果过程 |
| 176 题独立校准 | 标签歧义较低、数据集级参考标签可靠性 | 人类效标效度、human baseline 或 human ceiling |
| 不同标签来源的稳健性分析 | 部分缓解 annotation-family artifact 疑虑 | 建立对真实人的外部效度 |

建议在论文中明确加入以下边界句：

> **HEART-Bench does not validate or predict real human behavior; it measures agreement with expert-adjudicated persona-consistent references for controlled synthetic persona trajectories.**

## 三、推荐标题与 HEART 展开

### 推荐标题

最严格、最贴近实际操作化的版本：

> **HEART-Bench: Evaluating Memory-Grounded Persona-Consistent Action Selection in LLM Agents**

更简洁的版本：

> **HEART-Bench: Evaluating Memory-Grounded Behavioral Consistency in Controlled Synthetic Personas**

若使用第二个版本，必须在正文定义：`consistency` 指与专家参考标签的一致性，而不是心理测量学意义上的重测稳定性或人格稳定性。

### HEART 缩写

当前的 “Human-like Emotion and Agent Reaction Test” 本身仍然包含过度主张，建议改为：

> **H**istory-grounded **E**valuation of **A**gent **R**esponses over **T**ime

另一种做法是将 HEART-Bench 保留为品牌名称，不再展开缩写。

## 四、摘要建议稿

```text
Psychological theories provide useful structure for designing persistent
synthetic personas, but existing benchmarks rarely test whether LLM agents
use a persona's history when selecting actions. We introduce HEART-Bench,
a benchmark of psychology-informed, memory-grounded behavioral consistency
in controlled synthetic personas. HEART-Bench defines 11 personas using
Big Five and value-based specifications, assigns each 1,000 synthetic
autobiographical memories, and evaluates them in 64 DIAMONDS-guided
decision scenarios. Psychology experts review and adjudicate reference
responses, yielding 673 multiple-choice questions in which a model selects
the option most consistent with the predefined persona and its history.
We evaluate 12 frontier LLMs under a No-Retrieval baseline and three
memory-augmented settings. The strongest configuration reaches 63.3%
reference-label accuracy, while most models remain below 40%, indicating
substantial difficulty in memory-grounded persona reasoning within this
controlled setting. HEART-Bench does not validate or predict real human
behavior; it measures agreement with expert-adjudicated references for
synthetic persona trajectories.
```

## 五、Introduction 与研究问题

### 推荐研究问题

> **Given a controlled synthetic persona and its prior synthetic memories, can an LLM select the behavioral response that experts judge most consistent with that persona across diverse decision scenarios?**

### 推荐构念声明段落

建议放在 Introduction 中首次正式定义 HEART-Bench 的位置，而不能只放在 Limitations：

```text
Throughout this paper, psychology-informed describes the theoretical
frameworks used to construct the benchmark; it does not imply that the
synthetic personas instantiate human psychological processes. We
operationalize persona consistency as agreement between an agent's selected
option and an expert-adjudicated reference response conditioned on a
predefined synthetic profile, history, and scenario. Accordingly,
HEART-Bench does not validate or predict real human behavior, emotion,
or psychological state.
```

## 六、Contributions 建议稿

```text
\begin{itemize}[leftmargin=2em]
\item We introduce a controlled benchmark comprising 11
psychology-informed synthetic personas, 11,000 synthetic autobiographical
memories, 64 decision scenarios, and 673 expert-adjudicated MCQs.

\item We operationalize memory-grounded persona consistency as selecting
an expert-adjudicated reference response conditional on a predefined
persona, history, and scenario, and independently audit 176 items for
reference-label reliability.

\item We evaluate 12 LLMs across No-Retrieval and three memory-augmented
settings, quantifying their ability to use encoded persona and memory cues
within this controlled synthetic setting.
\end{itemize}
```

不建议继续使用：

- “evaluate LLMs' human-like psychology”；
- “the ability to exhibit human-like psychology remains limited”；
- “validated characters”。

其中 “validated characters” 可改为 “expert-reviewed synthetic personas” 或 “curated synthetic personas”。

## 七、方法中的操作化定义

建议将一个评测实例形式化为：

- (p_i)：预定义的合成人格规格；
- (h_i)：该人格的合成自传式历史；
- (s_i)：受控决策场景；
- (O_i)：候选响应集合；
- (y_i^*)：专家裁定的 keyed reference；
- \(\hat{y}_i\)：被评测模型选择的响应。

指标计算的是：

\[
\frac{1}{N}\sum_{i=1}^{N}\mathbb{I}[\hat{y}_i=y_i^*]
\]

它估计的是模型与 benchmark reference 的一致程度，不是：

\[
P(\text{real human action}\mid\text{person, history, situation})
\]

### 实例定义建议稿

```text
Each MCQ asks the model to select, from four candidates, the response
judged by experts to be most consistent with the predefined synthetic
persona, its synthetic history, and the scenario. We refer to this option
as the keyed reference; it is not an observed human behavioral outcome.
```

### 指标定义建议稿

```text
Reference-label accuracy is the proportion of items for which the model
selects the expert-adjudicated keyed option. It quantifies agreement within
HEART-Bench and should not be interpreted as a measure of human likeness.
```

## 八、全篇术语替换表

| 当前措辞 | 推荐措辞 |
|---|---|
| human-like psychology | psychology-informed persona consistency |
| human-like psychological consistency | memory-grounded persona consistency |
| ground truth / gold annotation | expert-adjudicated reference response |
| correct answer / correct option | keyed option / reference option |
| behavioral accuracy | reference-label accuracy |
| psychologically grounded entity | psychology-informed synthetic persona |
| validated characters | expert-reviewed synthetic personas |
| lived experiences | synthetic autobiographical history |
| autobiographical memories | synthetic autobiographical memories |
| expected behavioral response | expert-adjudicated persona-consistent response |
| response the character would most likely produce | response judged most consistent with the predefined persona |
| human validation | expert review and adjudication |
| human-like psychological reaction proxy | persona-consistent reference response in a synthetic scenario |
| Ground Truth Annotation | Reference Response Annotation |
| Benchmarks for Evaluating Agent Psychology | Benchmarks for Persona- and Psychology-Informed Agent Evaluation |

在首次出现后可以继续使用 `accuracy`，但应先明确它是对 keyed reference 的准确率。

## 九、结果解释边界

结果数值和统计检验可以保留，但解释必须限定在合成 benchmark 内：

1. 63.3% 表示与 expert-adjudicated key 的一致率，不表示模型具有 63.3% 的人类心理能力。
2. 低分支持“模型难以利用合成人格中编码的记忆、价值和人格线索”，不支持“模型缺乏真实人类心理”。
3. 记忆消融支持模型对 persona/history assignment 的敏感性，不证明真实人类心理机制或因果关系。
4. 标签来源分析只能缓解模型家族来源偏差，不能建立真实人类效标效度。
5. 专家一致率不能被称为 human performance、human baseline 或 human ceiling。
6. “current LLMs struggle” 应限定为 “the evaluated models struggle within this controlled benchmark”。
7. “remaining headroom” 指相对于专家参考标签的空间，而不是相对于真实人类心理能力的空间。

## 十、176 题独立校准的正确表述

当前独立校准能够支持：

- 多数专家能够识别既有 keyed option；
- MCQ 的附加歧义总体有限；
- 参考标签具有数据集级可靠性；
- 一部分题目需要轻微措辞修订。

它不能支持：

- keyed option 是真实人类会采取的唯一行为；
- benchmark 具有真实人类心理效标效度；
- 专家成绩代表人类表现上限；
- 全部 673 题都经过独立逐题验证；
- 专家评审将模型生成标签转化成了客观心理事实。

建议继续保留如下限定：

> **The audit measures agreement with the existing reference labels and does not constitute validation against observed human behavior.**

同时，将 `independent calibration` 明确称为 `independent reference-label audit` 会更加准确。

## 十一、Conclusion 建议稿

```text
We introduced HEART-Bench, a controlled benchmark for evaluating whether
LLM agents select behavioral responses consistent with predefined synthetic
personas and their synthetic autobiographical histories. Across 12 LLMs and
four retrieval settings, the results reveal substantial differences in
reference-label accuracy and show that persona and memory assignments affect
model decisions. These findings characterize memory-grounded persona
reasoning within a controlled synthetic setting; they do not establish
human-like psychology, genuine emotion, or predictive validity for real
human behavior. Future work should connect this controlled evaluation to
behavioral data from real individuals and more diverse cultural and
demographic settings.
```

建议删除或收窄：

- “the first comprehensive benchmark”；
- “assessing human-like psychology”；
- “proxy for human-like psychological reaction”；
- “establish a new standard”。

若要保留 first/novelty 主张，应改成可核验的组合式主张，例如 “to our knowledge, the first benchmark combining X, Y, and Z”，并完成系统文献审计。

## 十二、Limitations 建议稿

```text
The central limitation of HEART-Bench is its construct scope. All personas,
memories, and decision contexts are synthetic, and the reference options are
expert-adjudicated responses to these predefined artifacts rather than
observed reactions from real individuals. Scores therefore assess
reference agreement and persona consistency within our controlled
construction; they do not establish human-like psychology, genuine emotion,
or predictive validity for human behavior. In addition, a single keyed
option compresses potentially multimodal behavior, even after ambiguity
screening. The 11 trait-anchored personas and 64 scenarios also limit
cultural and demographic generalization, while the 176-item audit estimates
reference-label reliability rather than independently validating every
item. Finally, expert-intensive annotation constrains benchmark scale.
Future work should collect real-person reference data and represent
behavioral uncertainty using response distributions rather than a single
deterministic label.
```

构念范围应作为第一项 limitation，而不是附带放在段落末尾。

## 十三、如果保留 human-like 主张，需要什么人类参照实验

即使增加实验，也不建议继续使用笼统的 “human-like psychology”。应先明确目标是：

1. 与真实人物选择一致；
2. 与人类对合成人格的判断一致；
3. 被人类感知为自然或像人；
4. 预测真实世界行为。

这四种目标需要不同证据，不能相互替代。

### 最低限度的真实人物效标设计

1. 招募真实参与者，收集经验证的人格量表、价值观和经过同意的个人历史信息。
2. 让参与者本人对 held-out 决策场景作答；参与者自己的回答作为效标。
3. 模型和人类预测者只能获得相同的历史信息，避免不公平信息条件。
4. 使用 person-held-out evaluation，确保测试人物未参与模型条件构造或调参。
5. 对同一参与者采集多个时间点或相似场景回答，表示行为的不确定性和重测变化。
6. 使用软标签或响应分布，而不是假定每个场景只有一个确定的人类答案。
7. 统计分析以参与者为聚类单位，使用 participant-clustered bootstrap、混合效应模型或等价方法，避免将同一个人的多个场景错误地视为独立样本。
8. 进行收敛效度和区分效度检验，排除词汇重叠、文本风格、选项长度和生成模型来源等替代解释。
9. 在不同文化、语言和人口群体中复制，并在 held-out people 上报告结果。
10. 预注册主要假设、排除规则、统计单位和主指标。

### 不同人类实验能够支持的主张

| 人类实验 | 最多能够支持的主张 |
|---|---|
| 专家判断哪个选项最符合合成人格 | persona interpretability / content validity |
| 普通人扮演合成人格并选择选项 | agreement with human role-players |
| 人类评价回答是否“像人” | perceived human-likeness |
| 真实参与者回答假想场景 | agreement with human vignette responses |
| 预测真实参与者的观察性或有后果行为 | real-human behavioral predictive validity |

如果参与者只是回答假想 MCQ，论文最多可以声称与 human scenario responses 一致；若要声称真实行为，需要体验采样、观察性数据或具有实际后果的行为任务。

## 十四、建议的审稿回复

```text
We agree that our original wording overstated the construct validated by
HEART-Bench. Psychological theories guide the construction of our synthetic
personas and scenarios, but the current benchmark does not compare model
outputs against observed behavior from real individuals. We will therefore
reframe the benchmark throughout the title, abstract, introduction,
contributions, methods, results, and conclusion as evaluating
psychology-informed, memory-grounded consistency with controlled synthetic
personas. We will also replace “ground truth” with “expert-adjudicated
reference response,” define accuracy as reference-label agreement, and add
an explicit limitation that the results do not establish human-like
psychology or predictive validity for real human behavior. Establishing
human behavioral validity requires a separate real-person reference study,
which we identify as future work.
```

## 十五、主要修改位置

| 位置 | 当前风险 | 建议动作 |
|---|---|---|
| `main.tex:78` | 标题直接声称 human-like psychology | 更换标题 |
| `main.tex:88` | 摘要定义为 human-like psychological consistency | 使用新的摘要与范围声明 |
| `main.tex:102` | 研究问题仍是 psychologically consistent decisions | 改为受控合成人格条件下的 action selection |
| `main.tex:143` | HEART 展开及 benchmark 定义越界 | 重命名缩写并重写构念定义 |
| `main.tex:161-165` | 两条贡献直接声称 human-like psychology | 使用新的贡献列表 |
| `main.tex:188` | pipeline caption 使用 ground truth | 改为 reference-response annotation |
| `main.tex:197-206` | ground truth、psychologically grounded entity | 改为 expert reference、psychology-informed persona |
| `main.tex:251-268` | most likely、correct option、gold annotation | 改为 judged most consistent、keyed reference |
| `main.tex:322` | accuracy 定义为 correct answer | 定义 reference-label accuracy |
| `main.tex:327-394` | 结果可能被解释为心理能力 | 全部限定在 controlled benchmark 内 |
| `main.tex:404` | “Evaluating Agent Psychology” | 改为 persona-/psychology-informed evaluation |
| `main.tex:418` | first comprehensive、human-like proxy | 使用新的 Conclusion |
| `main.tex:420-422` | 构念限制没有被置于首位 | 使用新的 Limitations |
| `main.tex:498-511` | human-like evaluation、gold labels | 重定义 comparison dimensions |
| `main.tex:1050-1172` | 附录持续使用 gold/ground truth/correct | 系统替换为 reference terminology |
| `main.tex:1823` | Ground Truth Annotation 标题 | 改为 Reference Response Annotation |

## 十六、提交前检查清单

- [ ] 标题不再出现 human-like psychology。
- [ ] HEART 展开不再包含 Human-like Emotion。
- [ ] 摘要明确 synthetic persona 和证据边界。
- [ ] Introduction 给出正式、可操作化的构念定义。
- [ ] 研究问题与实际 MCQ 任务一致。
- [ ] Contributions 不再声称测量真实人类心理。
- [ ] `ground truth`、`gold`、`correct response` 已系统替换。
- [ ] Accuracy 已定义为 reference-label agreement。
- [ ] 63.3% 等结果没有被解释为心理能力比例。
- [ ] 消融结果没有被解释为人类心理因果机制。
- [ ] 176 题校准没有被称为 human baseline 或 external validity。
- [ ] Conclusion 明确不预测或验证真实人类行为。
- [ ] 构念范围被放在 Limitations 第一项。
- [ ] Related Work、图注、表头和附录术语同步修改。
- [ ] 如保留任何 human-like 表述，已明确它只表示 motivation 或 perception，而不是被验证的构念。

## 最终建议

在当前证据条件下，优先选择全面重构为 **psychology-informed synthetic persona consistency**，而不是仓促增加一个弱人类 baseline。局部修改 `main.tex:78` 和 `main.tex:418` 不足以解决问题；全文必须维持同一条“构念—操作化—证据—主张”链条。
