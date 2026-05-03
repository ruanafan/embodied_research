---
tags: [EmbodiedAI, Robotics, Imitation_Learning, DAgger, Human_In_The_Loop]
last_updated: 2026-05-03
source: [Zotero, Local, Web]
status: [Draft]
---

# HG-DAgger: Interactive Imitation Learning with Human Experts

## 文献信息
- Title: HG-DAgger: Interactive Imitation Learning with Human Experts
- Authors: Michael Kelly, Chelsea Sidrane, Katherine Driggs-Campbell, Mykel J. Kochenderfer
- Date: 2019
- DOI: `10.1109/ICRA.2019.8793698`
- Zotero: `zotero://select/library/items/8B3EF6E3`
- Local raw file: [paper.pdf](../../raw/hg_dagger_interactive_imitation_learning_with_human_experts/paper.pdf)
- Local reference implementation: `/Users/ruanyifan/code/RLinf`，remote `https://github.com/RLinf/RLinf.git`，commit `6fb1d3fdf694b59550f500c81c057343e71871b5`

## 1. 研究问题
标准 DAgger 让 novice policy 参与数据采样，但这会带来 training-time safety 风险，也会降低 human expert label 质量。HG-DAgger 要解决的问题是：在保持 on-policy state distribution 优势的同时，如何让 human expert 只在必要时接管，并收集高质量 recovery demonstrations。来源：Zotero item `8B3EF6E3` 与本地 PDF Sections I/II。

## 2. 核心贡献
1. 提出 human-gated control scheme：novice policy 默认执行，expert 在观察到 unsafe state 时接管，恢复到 safe region 后再交还 novice。
2. 只在 expert 有连续控制权的 recovery segments 中记录 expert labels，从而避免 shared control 或 lag-induced labels 降低标签质量。
3. 使用 ensemble policy 的 output covariance 定义 novice doubt，并从 human interventions 中学习 risk threshold $\tau$。
4. 在 simulation 与 physical vehicle driving task 中，相比 DAgger 和 behavior cloning，表现出更稳定的 learning curves 和更好的 safety metrics。来源：本地 PDF Sections II-IV。

## 3. 方法概述
HG-DAgger 训练一串 novice policies。第 $i$ 个 training epoch 中，系统 rollout 一个 expert-novice combined policy：

$$
\pi_i(x_t)=g(x_t)\pi_H(x_t)+(1-g(x_t))\pi_{N_i}(o_t)
$$

其中 $g(x_t)=1[x_t \notin P]$ 表示 human expert 判断当前状态不在 permitted set 中时接管。每个 epoch 结束后，将 intervention/recovery segments 中的 expert labels 加入 aggregated dataset $D$，并训练下一个 novice policy。来源：本地 PDF Algorithm 1 与 Section II。

## 4. 实验设置
- 任务：两车道道路中的 obstacle avoidance / lane weaving。
- 初始化：先用 10,000 expert action labels 训练 behavior cloning policy。
- 后续训练：额外 5 个 training epochs，每个 epoch 累积 2,000 expert labels。
- 对比方法：Behavior cloning、DAgger、HG-DAgger。
- 真实车平台：SAIC MG-GS，使用 LiDAR 和 high-fidelity localization；安全驾驶员持续监控。来源：本地 PDF Section III。

## 5. 关键指标或结果
- 在 simulation 中，HG-DAgger 的 road departure rate 与 collision rate learning curves 比 DAgger 更稳定。
- 在 on-vehicle test 中，HG-DAgger novice 的 collisions 和 road departures 最少；其 steering angle distribution 相比 DAgger 更接近 human driving data。论文提醒真实车测试数据有限，应主要作为 heuristic evidence。来源：本地 PDF Section IV。

## 6. 单次迭代耗时线索
原始 HG-DAgger 论文没有报告每个 epoch 的 wall-clock time。它明确给出的 iteration granularity 是：

- 1 个 epoch = 多个 rollouts 中收集新的 intervention labels + 将 $D_i$ 加入聚合数据集 + 训练 $\pi_{N_{i+1}}$。
- 实验中每个 epoch 额外累积 2,000 expert labels。
- 论文没有给出 label sampling frequency、每个 rollout 的长度、每轮 retraining time，因此无法把 2,000 labels 稳健换算为分钟或小时。

在 SOP 中，HG-DAgger 被改造成 continuous streaming + asynchronous updates：intervention segments 被持续写入 shared buffer，cloud learner 频繁消费并更新 policy，而不是保留原始论文那种离散 5-epoch 节奏。来源：[SOP: Scalable Online Post-Training System](sop-scalable-online-post-training-system.md)。

## 7. 本地参考实现
本地 RLinf 仓库 `/Users/ruanyifan/code/RLinf` 可作为 HG-DAgger 的工程参考实现；它不是 Kelly et al. 原论文的 official/original implementation，而是将 human-gated DAgger 思想落到 Franka、OpenPI、LeRobot 和 Ray 异步训练栈中的参考流程。来源：本地 RLinf 仓库 commit `6fb1d3fdf694b59550f500c81c057343e71871b5`。

- 文档入口：`/Users/ruanyifan/code/RLinf/docs/source-zh/rst_source/examples/embodied/hg-dagger.rst`
- 真机配置入口：`/Users/ruanyifan/code/RLinf/examples/embodiment/config/realworld_pnp_dagger_openpi.yaml`
- rollout 逻辑入口：`/Users/ruanyifan/code/RLinf/rlinf/workers/rollout/hf/huggingface_worker.py`
- 关键语义：`algorithm.dagger.only_save_expert: True` 表示只保存 expert 实际执行的 step，符合 HG-DAgger-style intervention data；`False` 时走 classic DAgger 风格的 expert relabeling 路径。来源：上述配置文件与 rollout worker。

## 8. 局限性
- HG-DAgger 依赖 human expert 能快速识别 unsafe state 并及时接管；原论文也明确指出这限制了其适用场景。
- 对于 VLA manipulation，SOP 使用的是 HG-DAgger 的交互式模仿学习思想，而不是原始 autonomous driving 实验设置。
- 原论文缺少 wall-clock iteration time，使其与 RECAP 或 SOP 的时间成本只能在 label/trajectory 粒度上比较。
- RLinf-HG-DAgger 是本地参考实现，不能作为原论文实验数字或实现细节的直接证据。

## 9. 来源与引用
- Zotero item: `8B3EF6E3`
- 本地 PDF 归档：[paper.pdf](../../raw/hg_dagger_interactive_imitation_learning_with_human_experts/paper.pdf)
- Web metadata: [Illinois Experts](https://experts.illinois.edu/en/publications/hg-dagger-interactive-imitation-learning-with-human-experts/)
- 本地参考实现：`/Users/ruanyifan/code/RLinf`，remote `https://github.com/RLinf/RLinf.git`，commit `6fb1d3fdf694b59550f500c81c057343e71871b5`

## 10. 相关页面
- 概念页：[Interactive Imitation Learning](../concepts/interactive-imitation-learning.md)
- 概念页：[Online Post-Training for VLA](../concepts/online-post-training-for-vla.md)
- 相关摘要：[SOP: Scalable Online Post-Training System](sop-scalable-online-post-training-system.md)
