---
tags: [EmbodiedAI, Robotics, VLA, Advantage_Modeling, RECAP, Robust_Manipulation]
last_updated: 2026-05-03
source: [Zotero, Local, Web]
status: [Draft]
---

# KAI0 Stage Advantage vs RECAP Value Function

## 1. 问题背景
KAI0 和 RECAP 都试图把“哪些行为更好”转化成 VLA policy 可消费的条件信号，但二者在 value function 上建模的对象不同。

RECAP 将 value function 作为 offline-to-online RL critic：先学习一个 language-conditioned distributional state value，再用 value difference 和 n-step returns 估计 action advantage，最后把 binarized advantage indicator 放入 VLA prefix。来源：[$\pi^*_{0.6}$](../summaries/pi-star-0-6-recap.md)、本地 RECAP PDF、Zotero item `JJIY4HUV`。

KAI0 的 Stage Advantage 更像阶段进度/偏好估计器：先人工标注 `stage_progress_gt`，训练模型直接预测两帧观测间的 progress delta，再把预测优势离散成 prompt 条件供 AWBC 使用。来源：[KAI0](../summaries/kai0-resource-aware-robust-manipulation.md)、Zotero item `MNPQV5ZH`、本地 `/Users/ruanyifan/code/kai0`。

## 2. 比较维度或分析框架

| 维度                    | RECAP / $\pi^*_{0.6}$                                                                                      | KAI0 / Stage Advantage                                                                              |
| --------------------- | ---------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| 被建模量                  | $p_\phi(V \mid o_t, \ell)$，语言条件的 distributional state value；返回分布离散为 `B = 201` bins                         | 两帧或阶段内的 progress/advantage；代码中训练目标为 `stage_progress_gt - his_-100_stage_progress_gt`                |
| 是否 action-conditioned | 不是 full Q-function；advantage 由 $r_{t:t+N-1} + V(o_{t+N}) - V(o_t)$ 推出，与数据中动作绑定                             | 也不是 full Q-function；更像 observation-pair progress estimator，后续用 frame-level advantage 对数据分 bin       |
| reward/progress 来源    | episode outcome rewards、autonomous rollouts、human corrections、demonstrations                               | 人工 stage boundary 与 `stage_progress_gt`，再由 estimator 预测 `relative_advantage` / `absolute_advantage` |
| policy 改进方式           | advantage-conditioned VLA training；positive indicator 进入 VLA prefix，可配合 CFG                                | Advantage-Weighted Behavior Cloning；离散后的 `task_index` 映射到语言 prompt，如 `Advantage: positive`          |
| 长时程处理                 | 通过 value function 传播 sparse terminal reward，并用 `N=50` lookahead 估计 post-training advantage                 | 将长任务拆成 semantic stages，在每个阶段内部做 progress/advantage 排序，降低跨阶段 value 差分噪声                              |
| 数据利用                  | demonstrations、failures、rollouts、interventions 都可进入 dataset；论文强调 advantage conditioning 不必丢弃低 advantage 数据 | 通过 percentile threshold 把 frame 标成 positive/negative 或 n-slices；低分数据仍在数据集中，但被 prompt 条件区分           |
| 主要风险                  | value coverage 不足、advantage 差分高方差、threshold/task tuning、batch/offline iteration 成本                         | stage annotation 成本、线性进度假设、prompt 离散化损失、对非 staged/open-ended task 泛化弱                               |

## 3. 结论
1. **RECAP 的 value function 更接近 RL critic，KAI0 的 Stage Advantage 更接近进度排序器。** RECAP 建模 return-to-go / time-to-completion 的分布，并用它推导 advantage；KAI0 直接监督“两个观测谁更接近当前阶段目标”，减少了先估 $V(s)$ 再相减的噪声。

2. **KAI0 在已知阶段结构的长时程任务上更稳，但理论泛化边界更窄。** 对 garment manipulation，阶段边界可由人类清楚定义，`stage_progress_gt` 能给 dense supervision，因此 Direct+Stage 的 MSTD/SFR 优势很自然。若任务没有稳定阶段、需要暂时后退、或成功路径高度多样，stage progress 可能把“必要绕路”误判为低 advantage。

3. **RECAP 的优势是能吃真实部署经验，缺点是 critic 覆盖成本高。** RECAP 可以把 autonomous failures、success/failure reward 和 human interventions 统一进 RL-style post-training；但一旦 value function 未覆盖目标任务分布，advantage indicator 会把错误 critic signal 注入 policy。SOP 对 RECAP 的讨论也指出 grocery restocking 这类语义泛化任务中，学习 sufficiently broad value function 仍困难。

4. **二者都刻意绕开了 full action-value Q-function。** RECAP 明确说当前 on-policy value estimator 比 classic off-policy Q-function 简单可靠，但不是最优；KAI0 则进一步把 signal 降维成 stage-aware observation-pair progress。二者的共同工程判断是：对大 VLA/flow-matching policy，稳定、可监督、可接入 BC 的 advantage signal 往往比端到端 Q-learning 更可落地。

5. **如果目标是资源高效、快速修补 production manipulation，KAI0 更合适；如果目标是从稀疏 reward 和失败经验中持续自我改进，RECAP 更完整。** 前者把难题转化为 stage annotation + AWBC，牺牲一部分 RL 普适性换取稳定和低资源；后者保留 RL 自改进闭环，但对 value training、数据覆盖和迭代基础设施要求更高。

## 4. 证据来源
- RECAP 摘要页：[$\pi^*_{0.6}$: a VLA That Learns From Experience](../summaries/pi-star-0-6-recap.md)
- KAI0 摘要页：[$\chi_{0}$: Resource-Aware Robust Manipulation](../summaries/kai0-resource-aware-robust-manipulation.md)
- Zotero items: `JJIY4HUV`、`MNPQV5ZH`
- RECAP 本地 PDF：[paper.pdf](../../raw/pi_star_0_6_a_vla_that_learns_from_experience/paper.pdf)
- KAI0 Web: [arXiv:2602.09021](https://arxiv.org/abs/2602.09021), [project blog](https://mmlab.hk/research/kai0)
- KAI0 local code: `/Users/ruanyifan/code/kai0`，commit `9d93078c757840f50e75248c5c5a94ab7b41e13a`

## 5. 潜在冲突或例外情况
- KAI0 论文/博客把 baseline 称为 `Value-diff` 或 $\pi^*_{0.6}$-style implementation；这不一定等价于 Physical Intelligence 原始 RECAP 的完整训练配方，尤其不等价于 RECAP 的大规模预训练数据和完整 iterative online collection。
- SOP 中的 RECAP implementation 与原始 RECAP 也不同：SOP Appendix 表示 value function offline pretrained 后在线阶段不更新。因此用 SOP-RECAP 的弱点直接归因到原始 RECAP 时必须谨慎。
- KAI0 的 `absolute_value` 字段名容易让人误解为 Bellman value；结合代码看，它是从初始帧到当前帧的 progress estimator 输出，不是 $V^\pi(s)$ 的严格 RL 语义。

## 6. 指向相关摘要页与概念页
- [KAI0 summary](../summaries/kai0-resource-aware-robust-manipulation.md)
- [RECAP summary](../summaries/pi-star-0-6-recap.md)
- [Advantage Modeling for VLA](../concepts/advantage-modeling-for-vla.md)
- [Offline-to-Online RL for VLA](../concepts/offline-to-online-rl-for-vla.md)
- [Online Post-Training for VLA](../concepts/online-post-training-for-vla.md)
