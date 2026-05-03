---
tags: [EmbodiedAI, Robotics, Reinforcement_Learning, VLA, Comparative_Analysis]
last_updated: 2026-05-03
source: [Zotero, Local]
status: [Draft]
---

# SOP 与 Learning while Deploying 对比（SOP vs Learning while Deploying）

## 1. 问题背景
两篇论文都研究 pretrained generalist VLA policy 如何在初始 pretraining 之后继续从物理世界中改进。它们共享从 deployment 到 learning 的 fleet-based closed loop，但贡献位于技术栈的不同层：
- SOP 主要贡献 online post-training system substrate。
- LWD 主要贡献运行在该 substrate 之上的具体离线到在线强化学习（offline-to-online RL）算法。

证据来源：
- [SOP: Scalable Online Post-Training System](../summaries/sop-scalable-online-post-training-system.md)
- [Learning while Deploying](../summaries/learning-while-deploying.md)

## 2. 比较维度

| 维度              | SOP                                                                   | Learning while Deploying                             |
| --------------- | --------------------------------------------------------------------- | ---------------------------------------------------- |
| 主要贡献            | 面向在线、分布式、多任务 VLA post-training 的系统框架                                  | 面向 continual policy improvement 的 RL 方法和部署循环         |
| 学习抽象            | 算法无关，可接入 HG-DAgger 或 RECAP                                            | 具体实例化为 DIVL + QAM 的 offline-to-online RL             |
| RL 的角色          | 通过 RECAP 支持的一种选项                                                      | 整篇论文的中心机制                                            |
| 数据循环            | actors 将 online trajectories 和可选 interventions stream 给 cloud learner | 同样是 broad actor-learner loop，但强调它作为 RL data flywheel |
| Offline data 使用 | 通过 adaptive sampling 与 online data 混合                                 | online training 时与 online data 以 1:1 混合              |
| Policy 类型       | shared generalist VLA policy                                          | shared generalist flow-based VLA policy              |
| 最强 claim        | fleet-scale infrastructure 支持快速、可扩展的 post-training                    | fleet-scale RL 能显著改善长时程真实世界 generalist policies      |

## 3. 结论
1. SOP 是更宽的系统论文。它回答如何搭建 actor-learner loop、adaptive sampling、policy synchronization 和 operational infrastructure。
2. LWD 是更尖锐的 RL 论文。它回答在目标是 generalist flow-based VLA policy 的稳定 offline-to-online RL 时，如何让这个循环发挥作用。
3. 如果研究问题是“如何在 fleet scale operationalize 真实世界 VLA online learning？”，SOP 是主要参考。
4. 如果研究问题是“如何在该循环之上做 robust RL，尤其是 long-horizon manipulation？”，LWD 是更强参考。

## 4. 证据来源
- SOP 明确表示它对 post-training algorithm 保持 agnostic，并用 HG-DAgger 和 RECAP 实例化系统。来源：Zotero item `5RX3IXG2`。
- LWD 明确围绕 DIVL value learning 和 QAM policy extraction 构建 learning method。来源：Zotero item `ZJSKS22S`。
- SOP 声称 fleet size 带来近似线性 scaling，并能在真实世界操作中实现 hours-scale post-training。来源：Zotero item `5RX3IXG2`。
- LWD 报告 8 个任务的 average success rate 为 `0.95`，且长时程任务 gains 尤其明显。来源：Zotero item `ZJSKS22S`。

## 5. 潜在冲突或例外情况
- 两篇论文总体上是互补关系，而不是互相矛盾。
- 一个细微张力在于：SOP 强调 algorithm agnosticism，而 LWD 暗示一旦稀疏奖励、off-policy replay 和 long horizons 成为主导因素，算法选择会非常重要。
- 另一个可能张力是 evaluation emphasis：SOP 强调 system scalability 和 deployment efficiency，LWD 强调 RL stability 和 long-horizon success。因此“最好”的方法取决于瓶颈是在基础设施还是 learning dynamics。

## 6. 实用阅读顺序
- 如果想先理解系统图景，先读 SOP。
- 如果想理解可能让系统在困难任务上更强的 RL mechanics，再读 LWD。
- 可以把 LWD 视为一个更专门的 realization，在概念上建立在 SOP formalizes 的 deployment substrate 之上。最后一句是基于论文内容和作者重叠的推断，不是显式依赖声明。

## 7. 相关页面
- [Learning while Deploying](../summaries/learning-while-deploying.md)
- [SOP: Scalable Online Post-Training System](../summaries/sop-scalable-online-post-training-system.md)
- [Online Post-Training for VLA](../concepts/online-post-training-for-vla.md)
