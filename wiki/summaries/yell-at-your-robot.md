---
tags: [EmbodiedAI, Robotics, VLA, Language_Feedback, Hierarchical_Policy]
last_updated: 2026-05-03
source: [Zotero, Local]
status: [Draft]
---

# Yell At Your Robot

## 文献信息
- Title: Yell At Your Robot: Improving On-the-Fly from Language Corrections
- Authors: Lucy Xiaoyang Shi, Zheyuan Hu, Tony Z. Zhao, Archit Sharma, Karl Pertsch, Jianlan Luo, Sergey Levine, Chelsea Finn
- Date: 2024-03-19
- DOI: `10.48550/arXiv.2403.12910`
- Zotero: `zotero://select/library/items/LQB24FII`
- Local raw file: [paper.pdf](../../raw/yell_at_your_robot_improving_on_the_fly_from_language_corrections/paper.pdf)

## 1. 研究问题
分层机器人 policy 能否通过学习部署期间人类给出的自然语言纠正，来改善长时程灵巧操作，而不依赖额外 teleoperation？来源：Zotero item `LQB24FII`，abstract 与 Section 1。

## 2. 核心贡献
1. 提出 YAY Robot：人类 verbal interventions 会临时覆盖 high-level policy，随后用于 post-train 该 high-level policy。
2. 展示自然语言既能监督实时恢复（real-time recovery），也能支持长时程任务的 continual improvement。
3. 展示一种基于 live narration 的轻量数据采集流程，避免昂贵的 post-hoc skill annotation。
4. 将 high-level post-training 重新表述为在 language actions 上进行的 HG-DAgger-like 过程，而不是 motor actions 上的过程。来源：Zotero item `LQB24FII`，abstract 与 Sections 3/4。

## 3. 方法概述
系统使用两个 policies：
1. low-level language-conditioned behavior cloning policy，执行一组细粒度技能。
2. high-level policy，预测下一步应发送给 low-level policy 的语言指令。

部署期间，人类可以说 "move a bit to the left" 或 "use the sponge to open the bag wider"。用户命令会立即覆盖 high-level prediction，实现 on-the-fly correction。该 intervention 被存入 correction dataset `D_corr`，之后 high-level policy 在 `D ∪ D_corr` 上 fine-tune，而 low-level policy 保持冻结。来源：Zotero item `LQB24FII`，Section 3。

架构上，high-level model 从短视觉历史中预测 language embedding，并从 dataset language bank 中检索 nearest-neighbor command。图中报告了 `History Length = 4`、DistilBERT language embeddings，以及 command space 上的 nearest-neighbor retrieval。来源：Zotero item `LQB24FII`，Figure 4 与 Section 3。

## 4. 实验设置
- 硬件：ALOHA-style 双臂系统。
- 任务：把物品装入 ziploc bag、准备 trail mix、清理盘子上的 gummies。
- 基础数据采集：teleoperator 通过麦克风实时叙述 intended skill，然后执行；Whisper 用于转写并同步 narration。
- 基础数据规模：
  - Bag packing：`1170` trajectories，`41517` skill segments，`1054` unique commands。
  - Trail mix：`317` trajectories，`7008` skill segments，`104` unique commands。
  - Plate cleaning：`265` trajectories，`3236` skill segments，`33` unique commands。
- post-training correction dataset 规模：
  - Bag packing：`3` iterations 后有 `2028` correction segments。
  - Trail mix：`3` iterations 后有 `292` correction segments。
  - Plate cleaning：`2` iterations 后有 `348` correction segments。来源：Zotero item `LQB24FII`，Section 4 与 Appendix A/Table III-IV。

## 5. 关键指标或结果
- 实时 verbal corrections 将长时程任务表现从 `15%` 提升到 `50%`。来源：Zotero item `LQB24FII`，abstract。
- 将收集到的 corrections 纳入 high-level post-training 后，表现从 `15%` 提升到 `45%`。来源：Zotero item `LQB24FII`，abstract。
- post-training dataset 只有 base dataset 约 `4%` 到 `11%` 的规模，说明少量 language-only correction data 仍可实质性改善 high-level policy。来源：Zotero item `LQB24FII`，Appendix A/Table IV。

## 6. 为什么重要
这篇论文清楚地说明，VLA-adjacent systems 的数据模型需要专门的 correction layer。如果监督只有 demonstration-to-action，系统就学不到用户如何自然修复失败、改变偏好或在轨迹中途重定向行为。来源：Zotero item `LQB24FII`，Sections 1/3/4。

## 7. 局限性
- post-training 期间 low-level policy 保持冻结，因此语言纠正只能改善 high-level instruction selection，不能改善 motor primitive 本身。
- 实验是 task-specific，并集中在单一硬件家族。
- 固定 language bank 上的 retrieval 可能限制开放式语言表达能力。
- 最强的定量 headline 是 aggregate success-rate improvement；若要升级到 `Verified`，仍应直接检查 figures 中的 per-task improvements。

## 8. 来源与引用
- Zotero item: `LQB24FII`
- 本地 PDF 归档：[paper.pdf](../../raw/yell_at_your_robot_improving_on_the_fly_from_language_corrections/paper.pdf)

## 9. 相关页面
- 概念页：[Hierarchical Language Supervision for VLA](../concepts/hierarchical-language-supervision-for-vla.md)
- 相关摘要：[Hi Robot](hi-robot.md)
- 相关摘要：[π0.5](pi0-5.md)
- 综合页：[VLA Data Annotation and Training](../syntheses/vla-data-annotation-and-training.md)
