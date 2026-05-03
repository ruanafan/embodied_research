---
tags: [EmbodiedAI, Robotics, UMI, VLA, Action_Tokenization, Cross_Embodiment]
last_updated: 2026-05-03
source: [Zotero, Local, Web]
status: [Draft]
---

# RDT2

## 文献信息
- Title: RDT2: Exploring the Scaling Limit of UMI Data Towards Zero-Shot Cross-Embodiment Generalization
- Authors: Songming Liu, Bangguo Li, Kai Ma, Lingxuan Wu, Hengkai Tan, Xiao Ouyang, Hang Su, Jun Zhu
- Date: 2026-02-03
- DOI: `10.48550/arXiv.2602.03310`
- Zotero: `zotero://select/library/items/T5QEAPEZ`
- Local raw file: [paper.pdf](../../raw/rdt2_exploring_the_scaling_limit_of_umi_data_towards_zero_shot_cross_embodiment_generalization/paper.pdf)
- Project: [rdt-robotics.github.io/rdt2](https://rdt-robotics.github.io/rdt2/)
- Local code: `/Users/ruanyifan/code/RDT2`
  - Remote: `https://github.com/thu-ml/RDT2.git`
  - Commit: `0797b4c65e588e088d41602685e00dc2bc95852f`
  - Key entry files: `train.py`, `main.py`, `vla_trainer.py`, `models/rdt/model.py`, `vqvae/models/rvq.py`, `deploy/inference_real_vq.py`, `deploy/inference_real_fm.py`

## 1. 研究问题
RDT2 把 UMI 系列从 data collection interface 推到 VLA foundation model：当 UMI-style robot-free demonstrations 扩展到 `10,000+` hours、`100+` indoor scenes 时，能否训练一个 zero-shot cross-embodiment generalist policy？关键挑战转成 action representation 与推理延迟：如何让 7B VLM 同时保留语言/视觉知识、输出可控连续动作，并足够快。来源：Zotero item `T5QEAPEZ`、项目页。

## 2. 核心贡献
- 重设计 UMI hardware，用更高强度材料与更稳定 tracking 支撑大规模采集。
- 收集 `10,000+` hours UMI demonstrations，覆盖 household/open-vocabulary manipulation。
- 提出三阶段训练：RVQ action tokenization 训练 VLM，flow-matching action expert 输出连续动作，single-step distillation 提升实时性。
- 以 UMI data 的 embodiment-agnostic end-effector interface 支撑 unseen objects/scenes/instructions/embodiments 的组合泛化。来源：本地 PDF Sections 4-5，项目页。

## 3. 轨迹数据获取
RDT2 的数据层沿用并增强 UMI：human demonstrator 用 embodiment-agnostic UMI device 采集 wrist-view images 与 continuous robot action chunks。项目页补充说新版硬件放弃原始 SLAM tracking，采用 HTC VIVE Tracker 3.0 infrared positioning 来获取 end-effector 6DoF pose，并通过统一 gripper/camera/end-effector 几何降低 embodiment gap。来源：本地 PDF Section 4，项目页 UMI Hardware。

论文的训练样本形式为 `D = {(l, o_t, A_t)}`，其中 `l` 是语言指令，`o_t` 是 RGB observation，`A_t = (a_t, ..., a_{t+Ta})` 是 action chunk。这里 trajectory data 已被整理成 language-conditioned imitation learning 样本，而不是每篇 UMI-style 系统中的 raw sensor stream 讨论。来源：本地 PDF Problem Formulation。

## 4. 多传感器对齐
RDT2 论文主文较少展开 raw sensor synchronization，默认 UMI hardware/pipeline 已将 wrist-view observations 与 action chunks 整理成可训练数据。大规模数据侧的关键是 hardware consistency 与 end-effector unification，而不是单篇系统中的 latency calibration 细节。来源：本地 PDF Section 4 与项目页。

部署时的对齐重点变成模型推理延迟与 action chunk 生成效率。RDT2 通过 RVQ 减少 autoregressive action tokens，并通过 flow-matching/distillation 减少 diffusion steps，解决 large VLA 在实时控制中的 latency pressure。来源：本地 PDF Sections 5.1-5.3 与项目页 Training。

## 5. State / Action 表征
RDT2 的 `state` 主要是 language instruction + RGB observation，即 `p(A_t | l, o_t)`；论文明确假设 `o_t` 已包含决策所需信息，不显式建模完整历史 observations。action 是一个 continuous action chunk，通常包含双手 6DoF end-effector pose 与 gripper width。来源：本地 PDF Section 3。

动作表征分三阶段演化：Stage 1 用 Residual Vector Quantization (RVQ) 把 continuous action chunk 压缩为少量 discrete action tokens，以适配 VLM next-token training；Stage 2 冻结 VLM backbone，训练 flow-matching RDT action expert 直接生成 continuous actions，降低 quantization error；Stage 3 distill 成 one-step generator，进一步降低 dynamic tasks 的 latency。项目页称 RVQ 能把 `0.8s`、`30Hz` action chunk 压缩成 `27` tokens。来源：本地 PDF Section 5，项目页 Training。

## 6. 局限性
- 论文把 raw trajectory acquisition/sensor sync 抽象成 UMI dataset pipeline，对底层采集误差、sensor drift 与 filtering 的细节披露少于 UMI/FastUMI。
- Stage 1 离不开 action tokenization 的 quantization trade-off，Stage 2/3 则依赖 diffusion/action expert 的训练稳定性与蒸馏质量。
- RDT2 的跨 embodiment 能力来自 UMI-style interface 与大规模数据，但遇到任务超出 gripper capability、需要五指 dexterity、水/热等场景时仍受硬件边界限制。来源：项目页 Dataset notes。

## 7. 相关页面
- 概念页：[State-Action Representation for UMI](../concepts/state-action-representation-for-umi.md)
- 概念页：[Cross-Embodiment Policy Interface](../concepts/cross-embodiment-policy-interface.md)
- 相关摘要：[Universal Manipulation Interface](universal-manipulation-interface.md)
- 综合页：[UMI Series Data Interface Overview](../syntheses/umi-series-data-interface-overview.md)

