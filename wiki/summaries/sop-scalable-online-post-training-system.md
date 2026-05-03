---
tags: [EmbodiedAI, Robotics, Reinforcement_Learning, VLA, Online_Post_Training]
last_updated: 2026-05-03
source: [Zotero, Local]
status: [Draft]
---

# SOP: Scalable Online Post-Training System

## 文献信息
- Title: SOP: A Scalable Online Post-Training System for Vision-Language-Action Models
- Authors: Mingjie Pan, Siyuan Feng, Qinglin Zhang, Xinchen Li, Jianheng Song, Chendi Qu, Yi Wang, Chuankang Li, Ziyu Xiong, Zhi Chen, Yi Liu, Jianlan Luo
- Date: 2026-01-06
- DOI: `10.48550/arXiv.2601.03044`
- Zotero: `zotero://select/library/items/5RX3IXG2`
- Local raw file: [paper.pdf](../../raw/sop_a_scalable_online_post_training_system_for_vision_language_action_models/paper.pdf)

## 1. 研究问题
如何把 VLA post-training 转化为物理世界中可运行的在线、分布式、多任务系统，使 generalist policies 能从真实部署经验中快速改进，同时不牺牲 generality？来源：Zotero item `5RX3IXG2`，abstract 与 introduction。

## 2. 核心贡献
1. 提出 SOP，一个把分布式机器人执行和集中式 cloud learning 耦合成闭环的系统框架。
2. 让 online post-training 与具体算法解耦，展示同一系统可支持 HG-DAgger 和 RECAP。
3. 证明 fleet-scale deployment 可随机器人数量近似线性降低 post-training wall-clock time。
4. 展示单个 shared policy 可在多样 manipulation tasks 上改进，同时保持 multi-task coverage。来源：Zotero item `5RX3IXG2`，abstract 与 Sections I/IV。

## 3. 方法概述
SOP 主要是系统贡献，而不是新的 RL algorithm。

它的循环包括：
1. 将当前 policy 广播给 distributed robot actors。
2. 收集 autonomous rollouts 与可选 human interventions。
3. 将数据 stream 到 cloud-side online buffer。
4. 从 online 和 offline buffers 中采样 mixed batches。
5. 应用 plug-in post-training algorithm。
6. 异步把更新后的 weights stream 回 actors。

论文用两类算法实例化 SOP：
- [HG-DAgger](hg-dagger.md)，用于 interactive imitation learning。
- [RECAP](pi-star-0-6-recap.md)，用于 reinforcement learning-based post-training。

本地 RLinf 仓库 `/Users/ruanyifan/code/RLinf` 可作为这两类 plug-in post-training 思想的工程参考实现入口，包含 HG-DAgger 与 RECAP 流程；它不是 SOP 论文的 official/original system implementation。来源：本地 RLinf 仓库 remote `https://github.com/RLinf/RLinf.git`，commit `6fb1d3fdf694b59550f500c81c057343e71871b5`。

adaptive sampling strategy 会在任务间保持均衡，同时根据近期 loss 为每个任务调整 online/offline mix。来源：Zotero item `5RX3IXG2`，Sections III 与 IV。

## 4. 实验设置
- 平台：Agibot G1 双臂机器人，配备三个 RGB cameras，并以 30 Hz joint-position control 运行。
- 计算：集中式 cloud learner，使用 8 NVIDIA H100 GPUs。
- 初始化：pretrained VLA policy，基于约 **160 小时 multi-task robot data** 调优。
- 论文明确强调的任务：cloth folding、box assembly 和 grocery restocking。
- 部署属性：asynchronous actor-learner loop，并在 episodes 之间的安全边界刷新 checkpoints。来源：Zotero item `5RX3IXG2`，abstract、Sections I/IV 与 Appendix A/C。

## 5. 关键指标或结果
- SOP 在真实世界任务上显著提升 pretrained VLA performance，同时保持一个 shared policy。来源：Zotero item `5RX3IXG2`，abstract。
- 论文称有效 post-training 可以在数小时真实世界交互内发生。来源：Zotero item `5RX3IXG2`，abstract 与 introduction。
- wall-clock efficiency 随机器人数量近似线性扩展。来源：Zotero item `5RX3IXG2`，abstract 与 introduction。
- SOP 据称优于 HG-DAgger 和 RECAP 的 non-SOP counterparts，success rate 往往达到 `2x` 或更高。来源：Zotero item `5RX3IXG2`，introduction。当前缓存文本未提取完整 per-task metric table，因此精确 per-task numbers 仍需直接核验 PDF figures。
- 默认 SOP+HG-DAgger scaling experiment 中，达到 `0.8` target success 的 time-to-target 随 actor 数下降：1 actor 为 `173.6 min`，2 actors 为 `126.5 min`，4 actors 为 `71.7 min`。来源：本地 PDF Table I。

## 6. HG-DAgger 与 RECAP 的迭代成本线索
SOP 使用两种 plug-in post-training algorithms：HG-DAgger 代表 interactive imitation learning，RECAP 代表 reinforcement learning-based post-training。两者在“单次迭代”上的关键差异是：原始算法的 iteration 定义不同，而 SOP 又把它们都改造成 continuous actor-learner loop。

SOP 在形式化上仍写成第 $k$ 轮 policy $\pi_{\theta_k}$ 执行、收集数据集 $D_k$、再更新到 $\pi_{\theta_{k+1}}$。但系统实现中：

- robot actors 在 episode boundaries 异步上传 rollouts 与 human interventions；
- cloud learner 持续从 online/offline buffers 采样 batch；
- learner 每 `25 training steps` 发布一次 updated model parameters；
- actors 获取最新 checkpoint 的端到端延迟通常为 seconds to tens of seconds，并在安全边界刷新 policy；
- 主实验默认分配 `3 hours / 180 minutes` wall-clock budget。

### 6.1 三种 iteration 口径

| 口径 | HG-DAgger | RECAP |
| --- | --- | --- |
| 原始算法的一次迭代 | 1 个 epoch：rollouts 中由 expert 接管并收集 labels，加入 aggregated dataset，再训练下一个 novice policy | 1 个 cycle：on-robot data collection，value function training，advantage-conditioned policy training |
| 原始论文给出的迭代规模 | 初始化 10,000 labels；随后 5 epochs，每 epoch 额外 2,000 expert labels | T-shirt/shorts laundry：每轮 300 trajectories / 4 robots；box assembly：每轮 600 autonomous + 360 intervention trials / 3 robots |
| 原始论文是否给 wall-clock | 未给 | 未给 |
| SOP 中的更新语义 | intervention segments 连续 stream 到 buffer，learner frequent asynchronous updates | fresh trajectories 连续进入 buffer，learner 运行 RECAP-style asynchronous updates |
| SOP 给出的时间线索 | 默认 SOP+HG-DAgger；每个实验 3 小时预算；fleet scaling 中 target success 0.8 的 time-to-target 为 173.6 / 126.5 / 71.7 min，对应 1 / 2 / 4 actors | SOP+RECAP 使用同一类 3 小时 post-training setup；Appendix 说明 value function offline pretrained 且在线阶段不更新；未单独报告 RECAP time-to-target |

### 6.2 可追溯结论

1. 如果按 SOP 的实验预算理解，两种算法在 SOP 主实验中都被放入 3 小时 wall-clock post-training budget；SOP+HG-DAgger 是默认设置，RECAP 作为替代 plugin 对比。
2. 如果按 SOP 的“达到目标性能”理解，论文只给了默认 SOP 设置下的 fleet scaling time-to-target：1 actor 为 `173.6 min`，2 actors 为 `126.5 min`，4 actors 为 `71.7 min`。由于默认算法是 SOP+HG-DAgger，这组数可以谨慎归到 SOP+HG-DAgger 的 evidence；SOP+RECAP 没有单独给 time-to-target。
3. 如果按原始算法 iteration 理解，HG-DAgger 的一轮是 `2,000 expert labels`，RECAP 的一轮是数百到近千 trajectories；两者都没有直接报告每轮 wall-clock time。
4. 按 episode timeout 粗估，RECAP 的 T-shirt/shorts laundry 每轮最多约 `4.2h` policy-side collection，box assembly 每轮最多约 `53.3h` policy-side collection。这是用 episode timeout 和 robot count 推出的保守上界，不含 reset、human waiting 和 GPU training。
5. RECAP 的“5-15 分钟任务时长”不能直接替代 timeout 估算：原文总体描述任务执行约 5-15 分钟，但 quantitative evaluation 又给出 200/500/600 s 的 task-specific timeout；因此当前估算采用与具体 success criteria 绑定的 timeout 口径。
6. SOP 的核心价值是压缩 iteration latency：HG-DAgger 不必等完整 epoch，RECAP 也不必等完整 batch redeploy；数据和参数更新以秒到分钟级系统循环持续发生，但论文没有给出单个 learner step 的秒数。

潜在例外是，RECAP 原论文主文称 box assembly 每轮为 `600 autonomous trials + 360 trials with interventions`，Appendix 的 dataset composition 又写成 `600 demonstrations + 360 correction episodes`。这里可能是术语使用不一致，暂按主文的 autonomous/intervention 表述作为主要依据。另一个差异是 SOP 中的 RECAP implementation 与原始 RECAP 不完全相同：SOP Appendix 说明 value function 在 online policy training 中不更新，而原始 RECAP iteration 通常包含 value function finetuning。

## 7. 为什么重要
SOP 的重要价值在于清晰分离关注点：
- system loop 定义真实世界数据和 policies 如何循环；
- learning algorithm 是可替换模块。

这个 abstraction 很有用，因为它把 fleet-scale post-training 变成可承载不同 online learning methods 的基础设施，其中也包括 RL。来源：Zotero item `5RX3IXG2`，Sections I 与 IV。

## 8. 局限性
- SOP 本身不是新的 RL objective；大部分算法 gains 仍取决于所选 plug-in method。
- 当前证据集中在一个实验室/部署 stack 和一个机器人平台。
- 缓存文本确认了 high-level results，但没有覆盖 figures 中每个精确定量细节；部分 claims 仍待直接图表核验。
- human intervention 仍是循环的一部分，因此系统并非纯自主。后三点部分来自论文设置推断。
- 对 RECAP 的 SOP implementation 与原始 RECAP 存在差异：SOP Appendix 说明 online training 阶段 value function 是 offline pretrained 且不随 policy training 更新。

## 9. 来源与引用
- Zotero item: `5RX3IXG2`
- 本地 PDF 归档：[paper.pdf](../../raw/sop_a_scalable_online_post_training_system_for_vision_language_action_models/paper.pdf)
- 本地参考实现：`/Users/ruanyifan/code/RLinf`，remote `https://github.com/RLinf/RLinf.git`，commit `6fb1d3fdf694b59550f500c81c057343e71871b5`

## 10. 相关页面
- 概念页：[Online Post-Training for VLA](../concepts/online-post-training-for-vla.md)
- 概念页：[Offline-to-Online RL for VLA](../concepts/offline-to-online-rl-for-vla.md)
- 概念页：[Interactive Imitation Learning](../concepts/interactive-imitation-learning.md)
- 比较综合：[SOP vs Learning while Deploying](../syntheses/sop-vs-learning-while-deploying.md)
- 相关摘要：[Learning while Deploying](learning-while-deploying.md)
- 相关摘要：[π*0.6: a VLA That Learns From Experience](pi-star-0-6-recap.md)
- 相关摘要：[HG-DAgger](hg-dagger.md)
