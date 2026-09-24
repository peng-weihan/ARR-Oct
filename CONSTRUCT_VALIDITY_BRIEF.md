# HEART-Bench 构念效度问题简报

## 核心问题

当前论文将 HEART-Bench 定位为对 LLM agent “human-like psychology” 或“类人心理一致性”的评测，但现有实验并未观测真实人物的心理状态或行为。基准实际要求模型根据预定义的合成人格、职业信息和检索到的合成自传体记忆，从四个候选行为中选择专家认为最符合该角色设定的选项。因此，当前任务直接测量的是**受控合成场景中、基于记忆的角色一致行为选择**，而不是模型是否具有类人心理，也不是模型能否预测真实人类行为。

这一差异属于构念效度问题，而不只是措辞问题。若标题、摘要和结论继续将 “human-like psychology” 作为被直接测量的对象，审稿人可能认为论文的证据不足以支持其主张范围。模型得分较低既可能反映其难以利用记忆推断角色一致行为，也可能来自输入信息不足、选项歧义、角色 ID 或职业泄漏、候选文本风格以及标签来源偏差。因此，当前结果不能被唯一解释为模型缺乏类人心理能力。

## 主要依据

首先，角色、记忆、场景和候选行为均为合成内容。Big Five、Schwartz 价值观和 DIAMONDS 等心理学框架为数据构造提供了理论结构，但这只能说明基准是 *psychology-informed*，不能证明合成角色呈现了真实人类的心理过程。

其次，专家评审验证的是候选行为与预定义角色档案之间的一致性，而不是候选行为与真实人物实际反应之间的一致性。现有准确率更适合解释为模型与 **expert-adjudicated reference response** 的一致率，即 *reference-label accuracy*。独立专家校准可以支持参考标签的可靠性，但不能被视为真实人类效标、human baseline 或 human ceiling。

再次，现有输入和数据构建仍可能包含替代性线索。职业与人格设定相关，部分角色 ID 可能编码人格极性，记忆字段也可能包含显式心理结论；同时，参与候选答案生成的模型家族也被用于最终评测。这些因素意味着模型可能利用身份、职业、语言风格或模型来源完成任务，而不必真正从自传体经历推断行为。

最后，当前实验是单轮四选一任务，不涉及多轮交互、状态更新、行动后果或长期行为稳定性。因此，它可以评估 memory-augmented LLM decision making，但单独使用该任务尚不足以支持更广泛的 “agent psychology” 主张。

## 潜在解决方案

投稿前最直接且成本最低的方案是统一收窄论文定位。标题、摘要、研究问题、贡献、结果解释和结论应将核心构念改为 **psychology-informed, memory-grounded persona consistency** 或 **memory-grounded persona-consistent action selection**。同时，应将 “ground truth”“gold answer” 和 “behavioral accuracy” 分别改为 “expert-adjudicated reference response”“keyed reference” 和 “reference-label accuracy”，并明确声明 HEART-Bench 不验证或预测真实人类行为。这样可以使构念、操作化、指标和结论保持一致，而不需要否定现有数据和主要实验结果。

为了进一步增强说服力，可以补充针对替代性解释的控制实验。优先级最高的是采用不透明角色 ID、隐藏职业、仅保留叙事记忆字段，并报告 ID-only、occupation-only、option-only、narrative-only、shuffled-memory 和 profile-oracle 等消融。若条件允许，还可增加不由被测模型家族生成的人工子集或留一模型家族评测，以缓解数据构建与模型评测形成闭环的风险。

若论文仍希望保留更强的心理一致性主张，则需要增加独立的人类参照证据。较可行的做法是在代表性子集上，让人类评估者与模型接收完全相同的信息，并比较双方对参考选项的选择；另一种做法是加入开放式行为生成及盲法专家评分，检验选择题得分与开放式评分之间的相关性。这些实验可以提供收敛效度或同信息条件下的人类参照，但仍不能直接证明模型具有真实心理。

## 建议定位

现阶段更稳妥的论文定位是：HEART-Bench 是一个结合心理学理论、合成自传体记忆和共享决策场景的受控基准，用于诊断 LLM 是否能够选择与预定义合成人格一致的行为。该定位保留了基准的核心贡献，同时避免将合成角色一致性过度外推为真实人类心理。

可在论文中加入如下操作化定义：

> We operationalize memory-grounded persona consistency as the ability to select the action that experts judge most consistent with a predefined synthetic persona, given its synthetic autobiographical history and a controlled decision scenario. This operationalization measures agreement with expert-adjudicated persona references rather than human psychological equivalence or predictive validity for real human behavior.
