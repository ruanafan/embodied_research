---
tags: [EmbodiedAI, Robotics, VLA, Reinforcement_Learning, Offline_to_Online_RL, Advantage_Modeling]
last_updated: 2026-05-03
source: [Zotero, Local, Web]
status: [Draft]
---

# VLA 的离线到在线强化学习（Offline-to-Online RL for VLA）

## 1. 定义
VLA 的离线到在线强化学习（offline-to-online RL for VLA）是指先用 demonstrations、historical rollouts、play data 或其他静态数据初始化 value/policy，再在真实部署中持续吸收 autonomous rollouts、success/failure outcomes 和 human interventions 来改进同一个 robot policy。来源：[Learning while Deploying](../summaries/learning-while-deploying.md)、[$\pi^*_{0.6}$](../summaries/pi-star-0-6-recap.md)。

## 2. 在具身智能中的作用
这种范式把部署从 evaluation phase 变成 continual data source。对具身系统而言，它尤其适合长时程、稀疏奖励和真实世界 distribution shift：失败轨迹、部分成功、恢复行为和人工接管不再只是需要过滤掉的噪声，而是用于 value learning 与 policy improvement 的证据。来源：[Learning while Deploying](../summaries/learning-while-deploying.md)、[SOP](../summaries/sop-scalable-online-post-training-system.md)。

## 3. 相关方法或代表性范式
- Offline RL initialization：在部署前用静态 buffer 建立稳定初始 policy/critic，降低在线阶段直接从稀疏奖励学习的风险。来源：[Learning while Deploying](../summaries/learning-while-deploying.md)
- RECAP：用 value function 估计 advantage，并训练 advantage-conditioned VLA policy；它是 $\pi^*_{0.6}$ 论文中的具体方法名，而不是本知识库中的独立概念页。来源：[$\pi^*_{0.6}$](../summaries/pi-star-0-6-recap.md)
- RLinf-RECAP：本地 `/Users/ruanyifan/code/RLinf` 提供 RECAP-style `compute returns -> value model SFT -> compute advantages -> CFG training` 参考流程，使用 `advantage_tag`、`positive_only_conditional` 和 `cfgrl_guidance_scale` 接入 OpenPI policy training；该仓库是参考实现，不是 Physical Intelligence 原论文 original implementation。来源：[$\pi^*_{0.6}$](../summaries/pi-star-0-6-recap.md)
- KAI0 Stage Advantage：不属于完整 offline-to-online RL loop，但与 RECAP 共享“把 advantage signal 变成 policy 条件”的接口；它用 stage-progress direct advantage 替代 value-diff critic，以牺牲一部分 RL 普适性换取长时程 staged tasks 上的数值稳定。来源：[KAI0](../summaries/kai0-resource-aware-robust-manipulation.md)、[KAI0 Stage Advantage vs RECAP Value Function](../syntheses/kai0-stage-advantage-vs-recap-value-function.md)
- DIVL + QAM：LWD 用 Distributional Implicit Value Learning 做 value estimation，用 Q-learning via Adjoint Matching 把 critic signal 提取到 flow-based VLA action generator。来源：[Learning while Deploying](../summaries/learning-while-deploying.md)
- Fleet-scale actor-learner loop：多台机器人并行生成 online experience，centralized learner 采样 offline/online buffers 并把更新后的 checkpoints 下发给 actors。来源：[SOP vs Learning while Deploying](../syntheses/sop-vs-learning-while-deploying.md)

## 4. 相关论文
- [Learning while Deploying](../summaries/learning-while-deploying.md)
- [$\pi^*_{0.6}$: a VLA That Learns From Experience](../summaries/pi-star-0-6-recap.md)
- [KAI0: Resource-Aware Robust Manipulation](../summaries/kai0-resource-aware-robust-manipulation.md)
- [SOP: Scalable Online Post-Training System](../summaries/sop-scalable-online-post-training-system.md)

## 5. 相关概念链接
- [Online Post-Training for VLA](online-post-training-for-vla.md)
- [Advantage Modeling for VLA](advantage-modeling-for-vla.md)
- [Interactive Imitation Learning](interactive-imitation-learning.md)
- [SOP vs Learning while Deploying](../syntheses/sop-vs-learning-while-deploying.md)

## 6. 争议点或开放问题
- 稀疏 reward 是否足以覆盖长时程 manipulation 中早期动作的 credit assignment，仍依赖 value learning 质量和数据覆盖。
- 在线 RL 是否会让 shared generalist policy 过拟合当前部署任务，并削弱未被持续练习的能力，需要持续评估。
- LWD、RECAP 和 SOP-RECAP 的训练循环粒度不同，比较 iteration cost 时必须区分原始算法 cycle、系统 checkpoint cadence 和完整 wall-clock budget。
- KAI0 提供了 stage-aware direct advantage 的替代路线，但它是否能替代 RL value learning，取决于任务是否有清晰阶段、人工进度标注是否可靠、以及是否需要从失败 rollouts 中学习 delayed reward。
