---
tags: [EmbodiedAI, Robotics, Imitation_Learning, Human_In_The_Loop, VLA]
last_updated: 2026-05-03
source: [Zotero, Local]
status: [Draft]
---

# 交互式模仿学习（Interactive Imitation Learning）

## 1. 定义
交互式模仿学习（interactive imitation learning）是在当前 policy 与真实或仿真环境交互时，让 expert 或 user 对 policy 访问到的状态提供 corrective labels、interventions 或 recovery demonstrations，并把这些数据聚合进后续训练。它比纯 behavior cloning 更关注 on-policy state distribution，也比纯 RL 更依赖人工纠错信号。来源：[HG-DAgger](../summaries/hg-dagger.md)、[Yell At Your Robot](../summaries/yell-at-your-robot.md)。

## 2. 在具身智能中的作用
在机器人系统里，interactive imitation learning 的价值在于把失败边界附近的状态转化为高质量监督。人类不必预先穷举所有 demonstrations，而是在 policy 快要失败、已经失败或需要重定向时提供接管、语言纠正或恢复动作。来源：[HG-DAgger](../summaries/hg-dagger.md)、[SOP](../summaries/sop-scalable-online-post-training-system.md)。

## 3. 相关方法或代表性范式
- DAgger：让 novice policy 诱导训练时状态分布，再从 expert 获取标签，以缓解 behavior cloning 的 covariate shift。
- HG-DAgger：human expert 在 unsafe 或 failure-prone states 接管控制，只记录 expert-controlled recovery segments；它是具体论文和方法名，不再作为独立概念页。来源：[HG-DAgger](../summaries/hg-dagger.md)
- Language correction loops：用户用自然语言覆盖或修正 high-level policy，随后将 correction segments 写入 post-training dataset。来源：[Yell At Your Robot](../summaries/yell-at-your-robot.md)
- SOP-HG-DAgger：SOP 将 human-gated interventions 连续 stream 到 shared buffer，并由 cloud learner 做 asynchronous updates。来源：[SOP](../summaries/sop-scalable-online-post-training-system.md)
- RLinf-HG-DAgger：本地 `/Users/ruanyifan/code/RLinf` 提供 Franka/OpenPI 场景的 HG-DAgger 参考实现入口，其中 `algorithm.dagger.only_save_expert: True` 表示只保存 expert 实际执行的 step；该仓库是参考实现，不是 HG-DAgger 原论文 original implementation。来源：[HG-DAgger](../summaries/hg-dagger.md)

## 4. 相关论文
- [HG-DAgger: Interactive Imitation Learning with Human Experts](../summaries/hg-dagger.md)
- [SOP: Scalable Online Post-Training System](../summaries/sop-scalable-online-post-training-system.md)
- [Yell At Your Robot](../summaries/yell-at-your-robot.md)
- [Hi Robot](../summaries/hi-robot.md)

## 5. 相关概念链接
- [Online Post-Training for VLA](online-post-training-for-vla.md)
- [Offline-to-Online RL for VLA](offline-to-online-rl-for-vla.md)
- [Hierarchical Language Supervision for VLA](hierarchical-language-supervision-for-vla.md)

## 6. 争议点或开放问题
- Human expert 能否足够及时、稳定地接管，是 interactive imitation learning 能否用于真实机器人安全闭环的关键瓶颈。
- 对 VLA systems 来说，纠正应该落在 high-level language/subtask 层，还是 low-level motor action 层，取决于失败来源。
- 人类接管数据通常分布在困难状态附近，如何在训练中平衡 correction data 与普通 successful trajectories，仍需要明确采样策略。
