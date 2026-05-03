---
tags: [EmbodiedAI, Robotics, AR, Data_Collection, Cross_Embodiment]
last_updated: 2026-05-03
source: [Zotero, Local, Web]
status: [Draft]
---

# ARCap

## 文献信息
- Title: ARCap: Collecting High-quality Human Demonstrations for Robot Learning with Augmented Reality Feedback
- Authors: Sirui Chen, Chen Wang, Kaden Nguyen, Li Fei-Fei, C. Karen Liu
- Date: 2024-10-11
- DOI: `10.48550/arXiv.2410.08464`
- Zotero: `zotero://select/library/items/WMFB9LJ6`
- Local raw file: [paper.pdf](../../raw/arcap_collecting_high_quality_human_demonstrations_for_robot_learning_with_augmented_reality_feedback/paper.pdf)
- Project: [stanford-tml.github.io/ARCap](https://stanford-tml.github.io/ARCap/)
- Local code: `/Users/ruanyifan/code/umi/ARCap`
  - Remote: `https://github.com/Ericcsr/ARCap`
  - Commit: `8fe21e533d2af8549b8c880ff331445dc0a42dbf`
  - Key entry files: `README.md`, `data_processing/data_collection_server.py`, `data_processing/convert_data_with_robot.py`

## 1. 研究问题
ARCap 不是 UMI 主线论文，但对本专题有价值：它研究 robot-free data collection 中如何通过 AR feedback 提前暴露 robot kinematic/collision/speed constraints，使 human demonstrations 更 robot-executable。来源：Zotero item `WMFB9LJ6`、本地 PDF。

## 2. 核心贡献
- 用 Quest 3 AR headset、Rokoko gloves、Quest controllers 和 RealSense D435 采集 portable demonstrations。
- 在 AR 中实时可视化 retargeted robot，并提供 camera visibility、joint/speed limit、collision warning。
- 支持 parallel-jaw gripper 与 dexterous hand 的 cross-embodiment retargeting。
- 输出可用于 diffusion policy/robomimic pipeline 的 point cloud、joint angle、headset pose 和 virtual robot pose。来源：本地 PDF Sections III-A/III-B。

## 3. 轨迹数据获取
ARCap 采集 user hands/wrists 的 motion，通过 controllers 获得 palm/wrist 6D pose，通过 Rokoko glove 获得 fingertip positions，通过 Quest SLAM 获得 headset/world frame，并用 D435 采集 colored point cloud。对 parallel-jaw gripper，action 由 index finger 与 thumb 的 midpoint、controller wrist orientation、open/close distance retarget 得到；对 dexterous hand，则用 fingertip matching + IK。来源：本地 PDF Section III-A。

## 4. 多传感器对齐
ARCap 的对齐策略是把数据统一到 AR world frame：point cloud、virtual robot pose、headset pose 和 retargeted joint states 都转换/存储到同一世界坐标。测试时，AR app 通过将 virtual robot base 与真实 robot base 对齐来简化 hand-eye calibration。来源：本地 PDF Section III-B 与 Fig. 5。

实时 feedback 是 acquisition-time validation：如果 virtual robot 跟不上 human hand、超速或与 scene map 碰撞，AR visualization 和 haptic warning 会让用户当场调整。这与 TAMEn 的 online feasibility check 在精神上相近，都是把 robot executability 前移到采集阶段。来源：本地 PDF Introduction/Section III-A。

## 5. State / Action 表征
ARCap 的 processed observation 包含 colored point cloud latent 和 current robot joint angle；action 是 target joint angles，包括 robot arm 和 hand。parallel-jaw gripper 的 gripper action 是 binary open/close，dexterous hand action 是 finger joint targets。来源：本地 PDF Section III-B。

这个表征偏 robot-native joint space，因为 ARCap 的目标是让 collected human motion 经 retargeting 后直接变成 robot-executable demonstrations。它不追求 UMI-style hardware-agnostic relative EE trajectory，而是用 AR feedback 在采集时约束 human motion，使 retargeted joint actions 更合法。来源：本地 PDF Sections I/III。

## 6. 局限性
- 需要 AR headset、glove、controller、D435 的多设备 calibration，部署复杂度不低。
- joint-space target 对具体 robot embodiment 更绑定；跨 embodiment 依赖 retargeting module。
- AR feedback 提高 executability，但不自动保证最终 policy 对 novel scenes/objects 的泛化。

## 7. 相关页面
- 概念页：[Robot-Free Trajectory Acquisition](../concepts/robot-free-trajectory-acquisition.md)
- 概念页：[Cross-Embodiment Policy Interface](../concepts/cross-embodiment-policy-interface.md)
- 相关摘要：[ActiveUMI](activeumi.md)
- 相关摘要：[TAMEn](tamen.md)
- 综合页：[UMI Series Data Interface Overview](../syntheses/umi-series-data-interface-overview.md)

