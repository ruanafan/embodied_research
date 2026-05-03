---
tags: [EmbodiedAI, Robotics, VLA, Reinforcement_Learning, Continual_Learning, Advantage_Modeling]
last_updated: 2026-05-03
source: [Zotero, Local, Web]
status: [Draft]
---

# VLA 的在线后训练（Online Post-Training for VLA）

## 1. 定义
VLA models 的在线后训练（online post-training）是指在部署后利用新收集的真实世界交互数据持续改进 pretrained robot policy，而不是把部署视为固定的 evaluation phase。

## 2. 在具身智能中的作用
对具身系统而言，部署会暴露离线数据集遗漏的真实 distribution shift：新物体、新布局、新用户、失败状态和恢复情境。online post-training 的目标是把这些差距转化为学习信号。来源：
- [Learning while Deploying](../summaries/learning-while-deploying.md)
- [SOP: Scalable Online Post-Training System](../summaries/sop-scalable-online-post-training-system.md)

## 3. 相关方法或代表性范式
- 交互式模仿学习（interactive imitation learning）：使用人类对当前 policy 访问状态的纠正。SOP 以 [HG-DAgger](../summaries/hg-dagger.md) 实例化这一范式。来源：[SOP: Scalable Online Post-Training System](../summaries/sop-scalable-online-post-training-system.md)、[Interactive Imitation Learning](interactive-imitation-learning.md)
- 离线到在线强化学习（offline-to-online RL）：把静态 offline replay 与在线部署数据结合，用于 continual policy improvement。RECAP 和 LWD 都属于相关代表。来源：[π*0.6](../summaries/pi-star-0-6-recap.md)、[Learning while Deploying](../summaries/learning-while-deploying.md)、[Offline-to-Online RL for VLA](offline-to-online-rl-for-vla.md)
- 优势建模（advantage modeling）：把 value、progress 或 pairwise preference 转成 VLA 可消费的 prefix/prompt 条件。RECAP 偏 RL critic，KAI0 Stage Advantage 偏 staged progress estimator。来源：[Advantage Modeling for VLA](advantage-modeling-for-vla.md)、[KAI0 Stage Advantage vs RECAP Value Function](../syntheses/kai0-stage-advantage-vs-recap-value-function.md)
- 舰队规模 actor-learner 系统（fleet-scale actor-learner systems）：多台机器人采集数据，cloud learner 更新 shared policy。SOP 和 LWD 都依赖这一模式。来源：[SOP vs Learning while Deploying](../syntheses/sop-vs-learning-while-deploying.md)

## 4. 相关论文
- [Learning while Deploying](../summaries/learning-while-deploying.md)
- [SOP: Scalable Online Post-Training System](../summaries/sop-scalable-online-post-training-system.md)
- [π*0.6: a VLA That Learns From Experience](../summaries/pi-star-0-6-recap.md)
- [KAI0: Resource-Aware Robust Manipulation](../summaries/kai0-resource-aware-robust-manipulation.md)
- [HG-DAgger: Interactive Imitation Learning with Human Experts](../summaries/hg-dagger.md)

## 5. 相关概念链接
- 通用机器人策略（generalist robot policy）
- [离线到在线强化学习（offline-to-online reinforcement learning）](offline-to-online-rl-for-vla.md)
- [优势建模（advantage modeling）](advantage-modeling-for-vla.md)
- [交互式模仿学习（interactive imitation learning）](interactive-imitation-learning.md)
- 人类干预/纠正（human intervention / correction）
- 分布式 actor-learner training

## 6. 争议点或开放问题
- generalist policy 在多大程度的 online RL 之后会开始过拟合特定部署任务？
- shared policy 能否从 fleet data 中改进，同时不静默削弱那些在线阶段没有被练习到的能力？
- 对真实世界长时程、稀疏奖励 manipulation，合适的 reward design 是什么？
- 这些系统离开原始工业级 stack 后有多可复现？

## 7. 交叉链接
- 综合页：[SOP vs Learning while Deploying](../syntheses/sop-vs-learning-while-deploying.md)
- 摘要页：[SOP: Scalable Online Post-Training System](../summaries/sop-scalable-online-post-training-system.md)
- 概念页：[Offline-to-Online RL for VLA](offline-to-online-rl-for-vla.md)
- 概念页：[Advantage Modeling for VLA](advantage-modeling-for-vla.md)
- 概念页：[Interactive Imitation Learning](interactive-imitation-learning.md)
