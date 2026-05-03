---
tags: [EmbodiedAI, Robotics, Reinforcement_Learning, VLA, Offline_to_Online_RL]
last_updated: 2026-05-03
source: [Zotero, Local, Web]
status: [Draft]
---

# Learning while Deploying

## 文献信息
- Title: Learning while Deploying: Fleet-Scale Reinforcement Learning for Generalist Robot Policies
- Authors: Yi Wang, Xinchen Li, Pengwei Xie, Pu Yang, Buqing Nie, Yunuo Cai, Qinglin Zhang, Chendi Qu, Jeffrey Wu, Jianheng Song, Xinlin Ren, Jingshun Huang, Mingjie Pan, Siyuan Feng, Zhi Chen, Jianlan Luo
- Date: 2026-04-30
- Project page: [AGIBOT Finch LWD](https://finch.agibot.com/research/lwd)
- Zotero: `zotero://select/library/items/ZJSKS22S`
- Local raw file: [paper.pdf](../../raw/learning_while_deploying/paper.pdf)

## 1. 研究问题
pretrained generalist VLA policy 如何在真实世界部署期间继续改进，而不只依赖固定 offline demonstrations，同时还能在异构舰队规模数据下保持稳定？来源：Zotero item `ZJSKS22S`，abstract 与 main text。

## 2. 核心贡献
1. 提出 Learning While Deploying（LWD），一个面向 shared generalist VLA policy 持续 post-training 的舰队规模离线到在线强化学习（offline-to-online RL）框架。
2. 引入 Distributional Implicit Value Learning（DIVL），用于从异构、稀疏奖励、多模态部署数据中估计 values。
3. 使用 Q-learning via Adjoint Matching（QAM），把 policy improvements 提取到 flow-based VLA action generator 中。
4. 在 16 台双臂机器人和 8 个 manipulation tasks 上展示真实世界改进。来源：Zotero item `ZJSKS22S`，abstract 与 Sections I/IV。

## 3. 方法概述
LWD 运行两阶段循环：
1. 在静态 buffer 上进行 offline RL pretraining；buffer 包含 demonstrations、historical rollouts 和 human play data。
2. 使用 offline buffer 与新采集 deployment experience 的混合 replay，持续进行 online post-training。

RL stack 包括：
- Value learning：DIVL，是 IQL-style asymmetric value learning 的 distributional extension，目标是保留罕见 high-return modes，而不是把它们压成 scalar average。
- Policy extraction：QAM，将 critic gradients 转换为 flow-based policy 的稳定 local regression targets。

论文强调 offline 和 online 阶段使用同一 RL objective，以降低 pretraining 与 deployment-time adaptation 之间的 mismatch。来源：Zotero item `ZJSKS22S`，Sections I、III、IV 与 Appendix B/C。

## 4. 实验设置
- 机器人舰队：16 台双臂机器人。
- 任务套件：8 个真实世界 manipulation tasks。
- 任务类型：grocery restocking tasks，以及 Gongfu tea、fruit juicing、cocktail making 和 shoebox-related assembly 等长时程任务。
- 时程特征：部分任务需要 3 到 5 分钟执行。
- Offline data buffer：共 652.5 小时，包括 demonstrations、successful rollouts、failed rollouts 和 play data。来源：Zotero item `ZJSKS22S`，abstract、Section I 与 Appendix B/C。

## 5. 关键指标或结果
- online improvement 后，8 个任务的 final average success rate 达到 `0.95`。来源：Zotero item `ZJSKS22S`，abstract 与 Table V。
- gains 在长时程任务上最大，因为 RL 中的 reward propagation 比 pure imitation 更有用。来源：Zotero item `ZJSKS22S`，Section I。
- 在报告的 value-learning ablation 中，online DIVL 的 average success rate 为 `0.95`，而 online scalar expectile regression 为 `0.88`。来源：Zotero item `ZJSKS22S`，Table V。
- 报告的 8 小时、16 actor 运行共摄入 1,604 episodes；end-to-end episode-to-learner latency 为 `P50 41s / P99 148s`，model-to-actor latency 为 `P50 38s / P99 55s`。来源：Zotero item `ZJSKS22S`，Table VI。

## 6. 为什么重要
这项工作把问题从“训练后再部署”转为“将部署本身作为 continual RL data source”。它主张真实世界 fleet usage 可以为单个 generalist robot policy 形成 data flywheel，而不只是改善 specialist policies。来源：Zotero item `ZJSKS22S`，Section I。

## 7. 局限性
- 证据来自一个 deployment stack 和一个 hardware family；跨 embodiment 的泛化尚未建立。
- 稀疏二值 rewards 和重工程基础设施可能让复现变得困难。
- 论文强调保持 generality，但评估仍集中在 8 个 in-house tasks，而不是更广泛的外部 benchmark。
- 报告结论基于作者自己的 system stack；没有独立 replication。这些是基于论文设置的推断，不是显式作者 claim。

## 8. 来源与引用
- Zotero item: `ZJSKS22S`
- 本地 PDF 归档：[paper.pdf](../../raw/learning_while_deploying/paper.pdf)
- 项目页：[AGIBOT Finch LWD](https://finch.agibot.com/research/lwd)

## 9. 相关页面
- 概念页：[Online Post-Training for VLA](../concepts/online-post-training-for-vla.md)
- 概念页：[Offline-to-Online RL for VLA](../concepts/offline-to-online-rl-for-vla.md)
- 比较综合：[SOP vs Learning while Deploying](../syntheses/sop-vs-learning-while-deploying.md)
- 相关摘要：[SOP: Scalable Online Post-Training System](sop-scalable-online-post-training-system.md)
