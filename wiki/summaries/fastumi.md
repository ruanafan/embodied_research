---
tags: [EmbodiedAI, Robotics, UMI, Data_Collection, Policy_Interface]
last_updated: 2026-05-03
source: [Zotero, Local, Web]
status: [Draft]
---

# FastUMI

## 文献信息
- Title: FastUMI: A Scalable and Hardware-Independent Universal Manipulation Interface with Dataset
- Authors: Zhaxizhuoma, Kehui Liu, Chuyue Guan, Zhongjie Jia, Ziniu Wu, Xin Liu, Tianyu Wang, Shuai Liang, Pengan Chen, Pingrui Zhang, Haoming Song, Delin Qu, Dong Wang, Zhigang Wang, Nieqing Cao, Yan Ding, Bin Zhao, Xuelong Li
- Date: 2025-02-01
- DOI: `10.48550/arXiv.2409.19499`
- Zotero: `zotero://select/library/items/2NFRB2JQ`
- Local raw file: [paper.pdf](../../raw/fastumi_a_scalable_and_hardware_independent_universal_manipulation_interface_with_dataset/paper.pdf)
- Project: [fastumi.com/FastUMI](https://www.fastumi.com/FastUMI/)
- Local code: not found under `/Users/ruanyifan/code/`; use Zotero PDF and project page as primary sources.

## 1. 研究问题
FastUMI 关注原始 UMI 的部署成本与工程脆弱性：能否保留 UMI 的 robot-free trajectory acquisition 思路，同时把 tracking、hardware adaptation、dataset format 和 policy training pipeline 做得更 plug-and-play？来源：Zotero item `2NFRB2JQ`、arXiv `2409.19499`。

## 2. 核心贡献
- 用 decoupled hardware design 替代原始 UMI 对特定 gripper/robot component 的依赖。
- 用 RealSense T265 / equivalent tracking module 替代复杂 GoPro VIO pipeline，降低 calibration 与 parameter tuning 成本。
- 支持生成 TCP trajectories 与 joint trajectories，服务 DP、ACT 等不同 imitation learning algorithms。
- 开源超过 `10,000` 条 real-world demonstration trajectories，覆盖 `22` 个 everyday tasks。来源：本地 PDF Abstract/Sections II-III，项目页。

## 3. 轨迹数据获取
FastUMI 的原始数据由三类 stream 组成：GoPro wide-angle images、T265 6DoF pose tracking、ArUco marker-based gripper width。T265 提供高频 pose estimates，例如 200Hz；GoPro 负责 observation，不再承担主 tracking。gripper width 由两枚 ArUco markers 的 pixel distance 线性映射到实际开口宽度，若 marker 缺失则用镜像或插值补齐以保持连续。来源：本地 PDF Sections III-A/III-C。

从这些 raw inputs，FastUMI 派生三类训练轨迹：absolute TCP trajectory、relative TCP trajectory、absolute joint trajectory。absolute TCP 需要将 T265 坐标系对齐到 robot base，并加入 camera-to-gripper offset；relative TCP 由相邻 TCP frame 的 relative transform 构成；joint trajectory 则通过 URDF 和 IK 从 TCP poses 求解。来源：本地 PDF Data Preparation for Training。

## 4. 多传感器对齐
FastUMI 使用 ROS pipeline：camera node 记录 GoPro images，tracking node 记录 T265 poses，storage node 聚合到 HDF5。所有 sensor stream 用 unified ROS clock timestamp，多线程 buffer 独立处理 stream，再按最大公约频率 synchronized sub-sampling。论文例子中 GoPro 60Hz、T265 200Hz，系统保留每 3 帧中的 1 帧相机图像，并匹配 nearest T265 pose，可达到 sub-millisecond offset。来源：本地 PDF Raw Data Acquisition。

T265 drift 通过 reinitialization 和 loop closure 缓解；数据质量用 confidence、velocity、acceleration、relative orientation thresholds 检查。FastUMI 的对齐目标更偏工程可部署：减少 VIO tuning，牺牲部分原始 UMI 的自洽一体化 pipeline，换取更稳定的 sensor module 与更简单的多平台复用。来源：本地 PDF Raw Data Quality Assessment。

## 5. State / Action 表征
FastUMI 同时支持 joint action 与 TCP pose action。标准 ACT 预测 absolute joint trajectories，但 wrist/first-person view 中 robot arm 不可见，容易生成 kinematically invalid actions；FastUMI 因此提出 Smooth-ACT 用 GRU 平滑局部时间变化，并提出 PoseACT，将 action 改为 TCP pose prediction，结合 absolute 与 relative motion trajectories。来源：本地 PDF Section IV-C。

对 Diffusion Policy，FastUMI 继承原始 UMI 的 relative TCP trajectory prediction 与 latency matching，并加入 Depth Anything V2 生成 depth map，作为 depth-enhanced DP 的额外 visual signal。这样做的动机是 wrist fisheye RGB 缺乏显式 3D depth，precision tasks 容易受影响。来源：本地 PDF Section IV-D。

## 6. 局限性
- T265/替代 tracking module 降低 VIO 复杂度，但引入 dual-sensor synchronization、drift management 和传感器供应风险。
- joint trajectories 对具体 robot embodiment 更直接，但跨平台性弱；TCP trajectories 更通用，但需要 IK 与 feasibility checks。
- depth-enhanced DP 使用 learned depth post-processing，未等同于真实 depth sensor，精度仍取决于 depth model 与 fisheye preprocessing。

## 7. 相关页面
- 概念页：[Robot-Free Trajectory Acquisition](../concepts/robot-free-trajectory-acquisition.md)
- 概念页：[Multi-Sensor Synchronization for Robot Data](../concepts/multi-sensor-synchronization-for-robot-data.md)
- 概念页：[State-Action Representation for UMI](../concepts/state-action-representation-for-umi.md)
- 相关摘要：[Universal Manipulation Interface](universal-manipulation-interface.md)
- 综合页：[UMI Series Data Interface Overview](../syntheses/umi-series-data-interface-overview.md)

