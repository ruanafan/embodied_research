---
tags: [EmbodiedAI, Robotics, VLA, Hierarchical_Policy, Language_Feedback]
last_updated: 2026-05-03
source: [Zotero, Local]
status: [Draft]
---

# Hi Robot

## 文献信息
- Title: Hi Robot: Open-Ended Instruction Following with Hierarchical Vision-Language-Action Models
- Authors: Lucy Xiaoyang Shi, Brian Ichter, Michael Equi, Liyiming Ke, Karl Pertsch, Quan Vuong, James Tanner, Anna Walling, Haohuan Wang, Niccolo Fusai, Adrian Li-Bell, Danny Driess, Lachy Groom, Sergey Levine, Chelsea Finn
- Date: 2025-07-15
- DOI: `10.48550/arXiv.2502.19417`
- Zotero: `zotero://select/library/items/ICNQ3VW8`
- Local raw file: [paper.pdf](../../raw/hi_robot_open_ended_instruction_following_with_hierarchical_vision_language_action_models/paper.pdf)

## 1. 研究问题
机器人如何跟随开放式、多阶段、约束繁多的自然语言指令，并在执行过程中吸收情境化用户纠正，而不要求单个扁平 VLA 直接解析全部复杂性？来源：Zotero item `ICNQ3VW8`，abstract 与 Sections 1/4。

## 2. 核心贡献
1. 提出分层 VLM-to-VLA 系统，由 high-level VLM 将开放式 prompts 和 feedback 转换为原子级 low-level robot commands。
2. 引入 synthetic interaction data 生成方案，为机器人 skill segments 标注合理的用户 prompts、interjections 和机器人 responses。
3. 在单臂、双臂和移动双臂机器人上展示实时情境化 correction handling。
4. 证明 hierarchy 加 synthetic high-level supervision 在开放式指令跟随上优于 GPT-4o high-level control 和 flat VLA baselines。来源：Zotero item `ICNQ3VW8`，abstract、Sections 4/5 与 Figure 5。

## 3. 方法概述
Hi Robot 将控制分解为两层：
1. high-level policy `p_hi(\hat{l}_t | I_t, l_t)` 读取当前图像和用户 prompt 或 interjection，并预测原子级技能指令，例如 "pick up the lettuce"。
2. low-level VLA `p_lo(A_t | I_t, \hat{l}_t, q_t)` 以连续动作执行该原子指令。

high-level policy 每 1 秒重新运行一次，或在新用户交互到达时立即运行。这让系统能够对纠正保持响应，同时维持 low-level control 的速度。来源：Zotero item `ICNQ3VW8`，Sections 4.1/4.2。

在监督数据方面，论文从 teleoperated demonstrations 出发，将其切分为通常持续 1 到 3 秒的短技能，再使用 VLM 合成可能触发这些 skill labels 的高层用户 prompts 和机器人 utterances。来源：Zotero item `ICNQ3VW8`，Section 4.3 与 Appendix A。

## 4. 实验设置
- 机器人平台：UR5e 单臂、bimanual ARX，以及 Mobile ALOHA-style 移动双臂系统。
- 任务：table bussing、sandwich making 和 grocery shopping。
- 交互类型：多阶段指令、未见过的任务组合、情境化纠正和用户约束。
- 基础模型：high-level 和 low-level policies 都从 PaliGemma-3B 初始化；low-level controller 使用 `π0` 加 flow-matching action expert。
- 附录报告的 high-level training 细节：batch size `512`，learning rate `1e-5`，约 `2 hours` on `8 x H100`。来源：Zotero item `ICNQ3VW8`，Sections 4/5 与 Appendix B/C。

## 5. 关键指标或结果
- Hi Robot 在 table bussing、sandwich making 和 grocery shopping 上的 instruction accuracy 与 task progress 均优于 GPT-4o high-level control 和 flat VLA baseline。来源：Zotero item `ICNQ3VW8`，Figure 5。
- 论文称 Hi Robot 的平均 instruction accuracy 比 GPT-4o 高出超过 `40%`。来源：Zotero item `ICNQ3VW8`，Figure 5 caption 与 discussion。
- 定性比较显示，移除 synthetic data 会损害系统遵循用户约束的能力，即使 visual grounding 仍然较合理。来源：Zotero item `ICNQ3VW8`，Figure 6/7 discussion。
- 该论文最强的定量 claims 主要来自图表；当前缓存文本未提取所有 per-task percentages，因此细粒度数字仍需直接核验 PDF figures。

## 6. 为什么重要
这篇论文对 VLA data design 的关键启发是：仅有 low-level robot demonstrations 并不足以教会开放式指令跟随。额外的关键监督不是更多 motor data，而是一个由语言 grounding 的 skill labels、corrections 和 constraints 构成的中间层。来源：Zotero item `ICNQ3VW8`，Sections 1/4。

## 7. 局限性
- high-level 和 low-level policies 分开训练，因此 high-level model 并不直接知道哪些 commands 能被 low-level model 可靠执行。
- high-level behavior 部分依赖 prompt-engineered synthetic data 的质量。
- 附录明确提到 long-context instructions 上的失败，以及 low-level 对近处物体的一些 bias。
- 如果要把本页从 `Draft` 升级到 `Verified`，仍需人工核验 figure-level quantitative comparisons。最后一点是工作流备注，不是作者 claim。

## 8. 来源与引用
- Zotero item: `ICNQ3VW8`
- 本地 PDF 归档：[paper.pdf](../../raw/hi_robot_open_ended_instruction_following_with_hierarchical_vision_language_action_models/paper.pdf)

## 9. 相关页面
- 概念页：[Hierarchical Language Supervision for VLA](../concepts/hierarchical-language-supervision-for-vla.md)
- 相关摘要：[Yell At Your Robot](yell-at-your-robot.md)
- 相关摘要：[π0.5](pi0-5.md)
- 综合页：[VLA Data Annotation and Training](../syntheses/vla-data-annotation-and-training.md)
