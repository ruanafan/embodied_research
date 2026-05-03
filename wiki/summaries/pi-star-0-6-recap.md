---
tags: [EmbodiedAI, Robotics, VLA, Reinforcement_Learning, RECAP, Online_Post_Training, Advantage_Modeling]
last_updated: 2026-05-03
source: [Zotero, Local, Web]
status: [Draft]
---

# $\pi^*_{0.6}$: a VLA That Learns From Experience

## 文献信息
- Title: $\pi^*_{0.6}$: a VLA That Learns From Experience
- Method: RL with Experience and Corrections via Advantage-conditioned Policies (RECAP)
- Authors: Physical Intelligence et al.
- Date: 2025-11-19
- DOI: `10.48550/arXiv.2511.14759`
- Zotero: `zotero://select/library/items/JJIY4HUV`
- Local raw file: [paper.pdf](../../raw/pi_star_0_6_a_vla_that_learns_from_experience/paper.pdf)
- Local reference implementation: `/Users/ruanyifan/code/RLinf`，remote `https://github.com/RLinf/RLinf.git`，commit `6fb1d3fdf694b59550f500c81c057343e71871b5`

## 1. 研究问题
如何让 large-scale VLA model 在真实部署中利用 sparse reward、autonomous rollouts 和 expert teleoperated interventions 继续改进，而不是只依赖离线 demonstrations？论文把这个问题形式化为 RECAP：先用 offline RL 预训练可进行 advantage conditioning 的 generalist VLA，再在目标任务上通过 one or more iterations of on-robot data collection 进行 specialization。来源：Zotero item `JJIY4HUV` 与本地 PDF Sections I/IV/V。

## 2. 核心贡献
1. 提出 RECAP，将 demonstrations、on-policy autonomous collection 和 expert interventions 统一进同一个 RL-style post-training recipe。
2. 训练 large multi-task value function，用于失败检测、估计 task completion progress，并把 action advantage 二值化为 VLA prefix 中的 optimality indicator。
3. 将 $\pi_{0.6}$ 扩展为 $\pi^*_{0.6}$，使 policy 可以条件化于 advantage values，从而通过 value function 引导更优动作分布。
4. 在 laundry folding、box assembly 和 espresso making 等真实任务上提升 success rate 与 throughput；论文摘要称在部分困难任务上 throughput 超过翻倍，failure rate 约减半。来源：Zotero item `JJIY4HUV` abstract 与本地 PDF Figures 7-10。

## 3. 方法概述
RECAP 的一次标准 iteration 包含三步：

1. **Data collection**：运行当前 VLA，给每个 episode 标注 outcome labels，并可选地让 expert teleoperator intervenes 来提供纠正。
2. **Value function training**：用当前任务已收集的全部数据训练 value function $V^{\pi_{\mathrm{ref}}}$，使其能估计失败风险与 expected time to task completion。
3. **Advantage-conditioned policy training**：用 value function 估计 advantage，把 advantage indicator 写入 VLA 输入前缀，并训练 policy 表示相对 $\pi_{\mathrm{ref}}$ 更优的动作分布。

预训练阶段在大量 demonstration 数据上执行 value training 与 policy training；部署后再重复 data collection、value finetuning 与 policy finetuning。来源：本地 PDF Section IV。

## 4. 本地参考实现
本地 RLinf 仓库 `/Users/ruanyifan/code/RLinf` 提供 RECAP 的工程化参考流程；它不是 Physical Intelligence 原论文的 official/original implementation，也不能替代论文中的实验设置或原始代码。来源：本地 RLinf 仓库 commit `6fb1d3fdf694b59550f500c81c057343e71871b5`。

RLinf 的 RECAP 流程分为四个阶段：

1. `compute returns`：`/Users/ruanyifan/code/RLinf/examples/recap/process/compute_returns.py` 与 `examples/recap/process/config/compute_returns.yaml` 计算轨迹回报，写入 `meta/returns_{tag}.parquet`。
2. `value model SFT`：`/Users/ruanyifan/code/RLinf/examples/recap/value/train_value.py` 训练 value model，用于从图像和语言观察预测归一化回报。
3. `compute advantages`：`/Users/ruanyifan/code/RLinf/examples/recap/process/compute_advantages.py` 根据 `advantage.value_checkpoint`、`returns_tag` 和 `positive_quantile` 生成 `meta/advantages_{tag}.parquet`。
4. `CFG training`：`/Users/ruanyifan/code/RLinf/examples/recap/cfg/train_cfg.py` 与 `examples/recap/cfg/config/libero_cfg_openpi.yaml` 使用 `advantage_tag` 读取优势标签，并通过 `positive_only_conditional`、`unconditional_prob`、`cfgrl_guidance_scale` 控制 classifier-free guidance policy training。

该本地实现特别适合作为“如何把 RECAP-style advantage-conditioned policy training 接入 RLinf/OpenPI 工程栈”的实践入口，而不是 RECAP 论文实验数字的来源。

## 5. 实验设置
- Robot setup：静态双臂系统，每臂 6 DoF，parallel jaw grippers，50 Hz joint-position control，3 个 camera 视角。
- 任务：Laundry folding、Cafe double-shot espresso、Box assembly。
- 主文总体描述这些 realistic tasks 需要多个步骤，执行时长约 5-15 分钟；但 quantitative evaluation 对具体任务又设置了各自的 success timeout。
- 时间限制：T-shirt/shorts laundry 为 200 s；diverse laundry 为 500 s；cafe espresso 为 200 s；box assembly 为 600 s。
- Iterative improvement 实验：T-shirt/shorts folding 和 box assembly 都比较了 two iterations of RECAP。来源：本地 PDF Sections V/VI 与 Appendix。

## 6. 关键指标或结果
- T-shirt/shorts laundry：每个 iteration 在 4 台 robot 上收集 300 trajectories；第一轮已把 success rate 提到 90% 以上，第二轮主要继续提升 throughput。来源：本地 PDF Figure 10 与 Section VI-B.2。
- Box assembly：每个 iteration 使用约 600 autonomous trials 和 360 intervention trials；第二轮后 throughput 约达到 2x 改善，并且 success rate 持续提升。来源：本地 PDF Section VI-B.2。
- Failure mode removal ablation：两轮、每轮 600 trajectories 的 setting 可达到约 97% success rate。来源：本地 PDF Section VI-B.3。

## 7. 单次迭代耗时线索
论文没有直接报告“one RECAP iteration wall-clock time”。可追溯信息是每轮采集规模、机器人数量和 episode timeout，因此只能得到 policy-side data collection 的上界估计：

| 任务 | 每轮数据 | 机器人数量 | Episode 上限 | 仅按 timeout 推得的采集上界 |
| --- | --- | --- | --- | --- |
| T-shirt/shorts laundry | 300 trajectories | 4 | 200 s | $300 \times 200 / (4 \times 3600) \approx 4.2$ 小时 |
| Box assembly | 600 autonomous + 360 intervention trials | 3 | 600 s | $960 \times 600 / (3 \times 3600) \approx 53.3$ 小时 |
| Cafe espresso | 414 autonomous + 429 correction episodes | 未明确 | 200 s | 若单机器人顺序采集，上界约 $843 \times 200 / 3600 \approx 46.8$ 小时 |

这些估计不包含 environment reset、human operator 等待、value/policy GPU training，也不是论文直接给出的 wall-clock。它们更适合作为“按任务 timeout 推得的最保守采集时长上界”。来源：本地 PDF Sections V/VI 与 Appendix。

## 8. 局限性
- 原论文的 RECAP 是 batch-style iterative offline loop，SOP 将其在线化后，iteration 语义发生变化。
- 精确 wall-clock iteration time、value finetuning time、policy finetuning time 未报告。
- 论文存在两个时间口径：主文称 realistic tasks 约 5-15 分钟，evaluation protocol 又给出 task-specific timeouts；做耗时估算时必须声明采用哪一个口径。
- 对 RECAP 的表现高度依赖 value function 是否覆盖目标任务分布；SOP 论文在 grocery restocking 上也指出 RECAP 与 HG-DAgger 的差距可能来自 value function 覆盖不足。
- KAI0 论文将其 Stage Advantage 与 $\pi^*_{0.6}$-style value-diff advantage 进行对比，认为 direct stage-aware advantage 在长时程 staged garment tasks 上更稳定；但该对比不必然等同于原始 RECAP 完整 recipe 的全面否定。来源：[KAI0 Stage Advantage vs RECAP Value Function](../syntheses/kai0-stage-advantage-vs-recap-value-function.md)
- RLinf-RECAP 是本地参考实现，不能作为 Physical Intelligence 原论文 original implementation 或实验结果的直接证据。

## 9. 来源与引用
- Zotero item: `JJIY4HUV`
- 本地 PDF 归档：[paper.pdf](../../raw/pi_star_0_6_a_vla_that_learns_from_experience/paper.pdf)
- 本地参考实现：`/Users/ruanyifan/code/RLinf`，remote `https://github.com/RLinf/RLinf.git`，commit `6fb1d3fdf694b59550f500c81c057343e71871b5`

## 10. 相关页面
- 概念页：[Offline-to-Online RL for VLA](../concepts/offline-to-online-rl-for-vla.md)
- 概念页：[Online Post-Training for VLA](../concepts/online-post-training-for-vla.md)
- 概念页：[Advantage Modeling for VLA](../concepts/advantage-modeling-for-vla.md)
- 相关摘要：[SOP: Scalable Online Post-Training System](sop-scalable-online-post-training-system.md)
- 相关摘要：[KAI0: Resource-Aware Robust Manipulation](kai0-resource-aware-robust-manipulation.md)
- 对比综合：[KAI0 Stage Advantage vs RECAP Value Function](../syntheses/kai0-stage-advantage-vs-recap-value-function.md)
