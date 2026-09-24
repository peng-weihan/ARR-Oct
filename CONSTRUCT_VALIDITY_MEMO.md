# HEART-Bench 构念效度问题与修改建议

## 核心结论

当前论文将 HEART-Bench 定位为对 LLM agent“类人心理”或“类人心理一致性”的评测，但现有实验并未直接观测真实人类的心理状态或行为。该基准实际测量的是：模型能否根据目标角色标识、职业信息与检索到的合成自传体记忆，从四个模型生成的候选行为中，选出专家认为最符合预设合成角色档案的选项。因此，当前任务更准确的构念是“基于合成自传体记忆的角色一致行为推断”，而非广义的“类人心理”。

这一差异并非单纯的措辞问题。若论文继续使用“human-like psychology”作为标题、摘要与结论中的直接测量对象，审稿人很可能认为论文存在构念过度外推：模型低准确率既可能反映角色隐变量难以从有限记忆中恢复，也可能来自选择题歧义、输入泄漏、候选答案风格偏差或标签噪声，不能直接解释为模型缺乏类人心理。

## 声称构念与实际测量对象

论文在标题、摘要、引言与结论中多次使用“human-like psychology”“psychological consistency”和“personality-consistent behavioral reasoning”等表述（`main.tex:78, 87–88, 102, 143, 158–165, 417–422`）。这些表述暗示基准能够衡量模型是否表现出与人类相似的心理反应。

然而，基准中的角色、记忆、场景和候选行为均为合成内容。角色由 Big Five 向量、派生的 Schwartz 价值观、职业、自我价值逻辑与行为模板共同定义；记忆由 Claude 生成；场景由 Claude 扩展；标准答案候选由 Gemini、Claude 与 GPT 生成，再由专家筛选或修改；干扰项亦由 Claude 选择（`main.tex:202–268, 1059–1165`）。专家在这一流程中验证的是候选行为与预设角色定义之间的一致性，而不是候选行为与真实人类行为之间的一致性。

因此，HEART-Bench 当前具有较强的内容效度与表面效度：任务内容确实涉及人格、价值观、经历和情境决策，专家也确认了候选行为的合理性。但其构念效度仍不充分，因为论文尚未证明该选择题分数能够代表“类人心理”这一更广泛概念，也未证明分数主要来自对自传体经历的心理推理，而不是角色标识、职业、显式行为字段或语言风格等捷径。

## 主要构念效度威胁

### 1. 合成角色一致性不等于真实人类心理

全部数据均围绕人为设计的极端人格角色生成，且没有真实人物的纵向经历、真实行为选择或独立人类被试作为参照。专家认可只能说明某个答案与预设角色设定相符，不能证明该答案代表真实人类在相同情境下的典型反应。论文结论中的“proxy for human-like psychological reaction”应被视为待验证假设，而不是已被实验确认的结论。

最直接的修改是收窄任务定义。标题、摘要、引言、贡献列表与结论应统一使用“persona-consistent behavioral inference”或“memory-grounded persona-consistent decision”作为核心术语，并明确说明该基准使用合成角色来操作化这一构念。“Human-like psychology”可以保留为应用动机，但不应继续作为被直接测量的对象。

### 2. 数据构建与模型评测形成闭环

被评测的 Gemini、Claude 与 GPT 模型家族同时参与标准答案候选生成。673 个最终标签中有 497 个源自 Gemini 候选，而 Gemini-3.1-Pro 与 Gemini-3-Flash 又在最终评测中排名前两位（`main.tex:383, 1059–1063, 1102, 1338–1402`）。专家筛选可以提高心理合理性，但无法完全消除源模型的表达风格、自偏好或决策框架。

现有 GT-source 分层分析表明 Gemini 在非 Gemini 来源子集上仍然领先，这能说明其优势并非完全由同源标注造成，但不能证明来源偏差可以忽略。交互项不显著不等于偏差不存在，尤其是在来源分布高度不均衡、GPT 来源仅有 50 题的情况下。

建议增加来源独立的验证集。优先方案是在至少 100–200 题上由人类专家直接撰写候选行为，不使用任何被测模型家族生成的文本。次优方案是采用留一模型家族构建：评测某一模型家族时，标准答案与干扰项均不得来自该家族。所有主要结果还应报告来源均衡子集上的表现。

### 3. 输入可能泄漏被隐藏的人格特征

论文称评测时隐藏 Big Five、价值逻辑与行为模板，但模型仍接收角色 ID 和职业（`main.tex:319–320, 1222`）。职业被明确设计为与主导人格特征一致（`main.tex:206, 526–545`），附录示例还出现 `CHAR_04_C_LOW` 等直接编码人格极性的 ID（`main.tex:1077`）。因此，模型可能通过 ID 或职业推断隐藏人格，而非从自传体记忆中归纳角色。

记忆模式还包含 `psych_conclusion`、`behavior_policy` 与 `emotion_signature` 等心理字段（`main.tex:721–774`），但论文未说明评测时检索结果究竟保留哪些字段。“De-identified memories”只能说明人口属性或身份信息被处理，不能证明显式心理字段已被屏蔽。若这些字段被保留，任务可能退化为显式行为规则匹配；若这些字段已删除，则论文仍缺少精确且可复现的评测协议。

建议将主要评测条件改为严格匿名设置：使用不透明角色 ID，隐藏职业，仅向模型提供 `timeline` 与 `content_full` 等叙事字段，并公开完整的序列化格式和推理提示词。同时应报告 ID-only、occupation-only、narrative-only、full-memory、random-ID 与 shuffled-memory 消融，以量化每一种潜在捷径的贡献。

### 4. 选择题可能测量风格识别，而非经历推理

标准答案与干扰项来自不同合成角色对同一场景的模型生成回应。即使表面行为相近，不同角色的选项仍可能包含稳定的词汇、语气、句式和职业线索。模型可能通过角色风格分类完成任务，而不需要建立从经历到人格再到决策的推理链。

现有记忆消融进一步显示，任意同角色非目标记忆已经达到 34.5–34.9%，场景匹配的正确角色记忆为 39.9%（`main.tex:1276–1328`）。这说明一般角色身份信号可能解释了大部分高于随机水平的收益，而场景匹配经历只贡献约 5 个百分点。错误角色的场景匹配记忆使结果下降至 22.7%，甚至低于四选一随机水平，也表明强烈的冲突身份线索会主导判断。

建议增加 option-only、scenario-only、occupation-only、profile-only 与 lexical-style classifier 等基线，并对全部选项进行人工释义或跨模型重写，检查排名是否稳定。还应增加 profile oracle：直接提供完整 Big Five 与价值观档案，以估计选择题在理想角色信息下的可解性；随后比较 profile oracle、memory-only 与 profile-plus-memory，明确记忆究竟提供了多少独立信息。

### 5. 单一标准答案不足以表达心理决策的不确定性

心理与人格驱动的行为通常具有多解性，但当前基准将每道题压缩为单一正确选项。独立校准中，176 题只有 139 题得到三位专家一致支持，26 题得到二对一支持，11 题仅有一位专家支持原标签；尽管如此，审计过程没有更改任何 keyed answer（`main.tex:1167–1200`）。这些结果说明标签总体具有较高可靠性，但约 21% 的题目仍存在不同程度的专家分歧。

建议将全体一致题目定义为高置信核心集，并在主结果中同时报告 Core 与 Full 两套分数。对二对一或一对二的题目，应保留专家投票分布，使用软标签得分或至少报告对争议题的敏感性分析。论文还应报告 construction 阶段的 Fleiss’ κ、Krippendorff’s α 或其他标注者间一致性指标，而不仅是最终仲裁结果。

### 6. 缺少与同信息条件匹配的人类上限

现有专家校准主要验证原标签是否合理，但没有明确报告人类在与模型完全相同输入条件下完成 673 道选择题的准确率。标准答案构建专家能够看到完整角色档案、价值观与候选生成依据，而评测模型只接收角色标识、职业与检索记忆；二者信息条件并不对称。因此，63.3% 不能直接解释为模型距离“人类水平”仍有多大差距。

建议在分层抽取的 100–200 题上招募独立心理学专家或受过训练的标注者，并严格限制其输入与模型一致。应报告个体准确率、专家间一致性、人类多数票准确率以及人类与模型的差距。若人类在相同信息条件下也明显低于完整档案条件，则说明任务主要受信息不足限制，而非模型缺乏心理推理能力。

### 7. 单轮选择题不足以支持“agent psychology”

当前评测是一次性四选一任务，不包含多轮交互、状态更新、工具使用、行动执行或行为后果。因而，“LLM agents”“agentic settings”与实验形式之间存在构念不匹配。该任务可以评测 memory-augmented LLM decision making，但不能单独代表智能体在持续交互中的心理一致性。

最低成本方案是将全文的“LLM agents”收窄为“LLMs under memory-augmented decision settings”。更强的方案是在一个代表性子集上增加开放式行为生成与盲法专家评分，并比较选择题得分和开放式评分的相关性。若两者高度相关，才可为选择题作为 agent-level proxy 提供收敛效度证据。

## 修改优先级

### P0：投稿前必须完成

首先，应统一收窄构念表述，将核心任务定义为基于自传体记忆的角色一致行为推断，并同步修改标题、摘要、引言、贡献列表、实验结论与 Limitations。建议英文标题改为：

> **Do LLM Agents Infer Persona-Consistent Behavior from Autobiographical Memories?**

其次，应明确并清理评测输入。主要结果应基于不透明角色 ID、隐藏职业和仅叙事记忆字段的严格匿名设置，同时公开完整评测提示词、记忆序列化格式与输出解析规则。若严格设置下需要重新运行实验，应以该结果替换当前主表。

再次，应增加输入捷径控制，至少包括 ID-only、occupation-only、option-only、narrative-only、shuffled-memory 与 profile-oracle。缺少这些控制时，论文无法证明准确率主要来自对自传体经历的推理。

最后，应降低同族模型参与标准答案构建所造成的闭环风险。最有说服力的方案是建立独立人工撰写子集；若成本受限，则至少完成留一模型家族评测和来源均衡评测，并避免使用被测模型家族选择干扰项。

### P1：显著提高接收概率

应增加与模型信息条件完全一致的人类上限，并报告个体表现、多数票表现与标注者间一致性。应将高一致题目设为核心集，对争议题采用软标签或敏感性分析。

还应补充构念效度实验。收敛效度可通过比较选择题准确率与开放式行为生成的专家评分来检验；区分效度可通过证明模型分数不主要由职业、ID、选项风格或显式行为字段决定来检验；已知组效度可通过验证 profile oracle 能稳定区分高低人格极性来检验；测量不变性可通过选项释义、顺序重排和场景改写测试来检验。

Limitations 应明确承认合成角色向真实人类泛化的限制、Big Five 与 Schwartz 框架的文化范围、单一答案对心理多解性的压缩、同族模型构建偏差、职业与角色 ID 捷径，以及单轮选择题与长期 agent 行为之间的差距。Ethics Statement 应说明该基准不适用于临床诊断或真实用户心理评估，并讨论其在 AI companionship 与 persona cloning 场景中的误用风险。

## 建议用于论文的操作化定义

可在引言中加入如下定义，以明确测量边界：

> We operationalize persona-consistent behavioral inference as the ability to select the action that best aligns with a predefined synthetic persona, given autobiographical memories and a shared decision scenario. This operationalization evaluates consistency with expert-validated persona specifications rather than human psychological equivalence.

摘要中的结论建议改为：

> These results indicate that current LLMs remain limited in inferring persona-consistent behavioral choices from synthetic autobiographical memories.

结论中的贡献建议改为：

> HEART-Bench provides a controlled testbed for evaluating whether LLMs can infer trait-grounded behavioral choices from synthetic autobiographical memories across shared psychological scenarios.

## 预期修改后的论文定位

完成上述修改后，论文最稳妥的定位不是“首个衡量 LLM 类人心理的综合基准”，而是“一个将人格特征、自传体记忆与共享心理场景结合起来，用于诊断角色一致行为推断能力的受控基准”。这一定位更符合现有证据，也更容易与 KnowMe-Bench、CloneMem、PersonaMem 和 CharacterEval 等相关工作形成清晰、可辩护的差异。

如果严格匿名、仅叙事记忆条件下的模型排序仍然稳定，人工撰写或留一模型家族子集仍显示 Gemini 优势，且选择题得分与开放式专家评分显著相关，则论文才具备将结论进一步扩展到“心理一致性代理指标”的实证基础。
