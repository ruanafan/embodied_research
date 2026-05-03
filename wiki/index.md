---
tags: [EmbodiedAI, Robotics, Reinforcement_Learning, VLA, Advantage_Modeling]
last_updated: 2026-05-03
source: [Zotero, Local, Web]
status: [Draft]
---

# 具身智能知识库（Embodied AI Knowledge Base）

## 通用机器人策略的强化学习（Reinforcement Learning for Generalist Robot Policies）

### 论文摘要
- [Learning while Deploying](summaries/learning-while-deploying.md)：面向共享 VLA policy 的舰队规模离线到在线强化学习（offline-to-online RL），结合自主 rollouts 与可选的人类干预数据。
- [SOP: Scalable Online Post-Training System](summaries/sop-scalable-online-post-training-system.md)：面向 VLA models 的在线、分布式、多任务 post-training 系统框架，可接入 imitation learning 和 RL 插件。
- [π*0.6: a VLA That Learns From Experience](summaries/pi-star-0-6-recap.md)：提出 RECAP，用 advantage-conditioned policies 将 demonstrations、autonomous rollouts、reward feedback 和 expert interventions 结合到 VLA post-training；含 RLinf 本地 RECAP 参考实现入口。
- [χ0 / KAI0: Resource-Aware Robust Manipulation](summaries/kai0-resource-aware-robust-manipulation.md)：提出以 Model Arithmetic、Stage Advantage 和 Train-Deploy Alignment 驯服 `P_train`、`Q_model`、`P_test` 分布不一致的资源高效长时程衣物操作框架；含本地 `kai0` 论文代码入口。
- [HG-DAgger](summaries/hg-dagger.md)：提出 human-gated DAgger，用 human expert 接管失败/危险状态并收集 recovery demonstrations；含 RLinf 本地 HG-DAgger 参考实现入口。

### 概念页
- [Online Post-Training for VLA](concepts/online-post-training-for-vla.md)：解释 VLA models 中的 online post-training、舰队数据为何重要，以及 RL 在其中的位置。
- [Offline-to-Online RL for VLA](concepts/offline-to-online-rl-for-vla.md)：整理 LWD、RECAP、DIVL/QAM 与 advantage-conditioned policy learning 所属的离线到在线 RL 范式。
- [Advantage Modeling for VLA](concepts/advantage-modeling-for-vla.md)：比较 RECAP、KAI0 Stage Advantage、DIVL/QAM 等将 value/progress/advantage signal 接入 VLA policy learning 的方式。
- [Interactive Imitation Learning](concepts/interactive-imitation-learning.md)：整理 DAgger、HG-DAgger、人类接管、correction/recovery demonstrations 等交互式模仿学习机制。

### 综合页
- [SOP vs Learning while Deploying](syntheses/sop-vs-learning-while-deploying.md)：从问题设定、系统设计、RL 角色、规模和局限性比较两项工作。
- [KAI0 Stage Advantage vs RECAP Value Function](syntheses/kai0-stage-advantage-vs-recap-value-function.md)：深度比较 KAI0 与 RECAP 在 value/advantage function 建模对象、训练信号、policy extraction 和适用边界上的差异。

## 交互式与开放世界 VLA（Interactive and Open-World VLA）

### 论文摘要
- [Yell At Your Robot](summaries/yell-at-your-robot.md)：使用真实人类语言纠正实现即时恢复和 post-training 的分层机器人学习框架。
- [Hi Robot](summaries/hi-robot.md)：面向开放式指令跟随的 VLM-to-VLA 分层系统，使用合成高层交互监督。
- [π0.5](summaries/pi0-5.md)：异构联合训练（heterogeneous co-training）的 VLA，同时预测语义子任务和低层动作，以提升开放世界家庭场景泛化。

### 概念页
- [Hierarchical Language Supervision for VLA](concepts/hierarchical-language-supervision-for-vla.md)：说明 VLA systems 为什么常需要位于用户 prompt 与动作之间的 subtask、correction 和语义监督层。

### 综合页
- [VLA Data Annotation and Training](syntheses/vla-data-annotation-and-training.md)：面向 π0.5 类长序任务，整理 VLM/VLA 输入输出边界、数据标注 schema、样例与分阶段训练配方。
