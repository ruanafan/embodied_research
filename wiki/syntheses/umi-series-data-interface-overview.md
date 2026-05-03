---
tags: [EmbodiedAI, Robotics, UMI, Data_Collection, Policy_Interface, Synthesis]
last_updated: 2026-05-03
source: [Zotero, Local, Web]
status: [Draft]
---

# UMI 系列数据采集与 Policy Interface 综述

## 1. 问题背景
UMI 系列的共同主线不是某一种 gripper，而是一个更大的数据工程问题：如何把真实世界人类示范转成可训练、可部署、可跨 embodiment 的 robot policy data。用户当前关注的三个问题分别是：轨迹数据如何获取、多传感器数据如何对齐、训练时 `state / observation` 与 `action` 如何表征以及为什么。来源：[Universal Manipulation Interface](../summaries/universal-manipulation-interface.md)、[FastUMI](../summaries/fastumi.md)、[RDT2](../summaries/rdt2.md)。

## 2. 比较框架

| 工作 | Trajectory source | Sensor streams | Sync / alignment strategy | State / observation | Action representation | 设计原因与限制 |
| --- | --- | --- | --- | --- | --- | --- |
| [UMI](../summaries/universal-manipulation-interface.md) | GoPro visual-inertial tracking 恢复 EE pose；markers 估计 gripper width | Fisheye RGB, GoPro IMU, gripper width, robot proprioception at deployment | observation latency matching；timestamp interpolation；action latency compensation | RGB + relative EE pose history + gripper width | future relative EE trajectory + gripper width | 减少 global frame 依赖，支持跨硬件；SLAM/VIO 和 latency calibration 是瓶颈 |
| [UMI on Legs](../summaries/umi-on-legs.md) | UMI manipulation trajectories + simulation WBC tracking data | GoPro RGB, iPhone/body pose, robot joints/base state | camera-frame trajectory 转 task-frame；低频 policy 接高频 WBC | 高层 RGB；WBC 观测 joints/base/previous action/EE trajectory | task-frame EE trajectory；WBC 输出 joint targets | 解耦 manipulation policy 与 quadruped embodiment；one-way interface 无法反馈 reachability |
| [FastUMI](../summaries/fastumi.md) | T265 pose + GoPro images + ArUco gripper width | GoPro 60Hz, T265 200Hz, gripper markers | ROS unified clock；thread-safe buffers；nearest/sub-sampled matching；drift correction | FPV RGB, optional depth, TCP/joint context | absolute TCP, relative TCP, absolute joint trajectories；PoseACT/DP | 更 plug-and-play，支持 ACT/DP；T265 引入 drift/supply/sync 管理 |
| [ActiveUMI](../summaries/activeumi.md) | Quest controllers/headset 同步记录 left/right/head 6DoF poses | VR controllers, HMD, wrist cameras, head/top camera | Quest world frame；zero-point calibration；placeholder/haptic feedback | wrist views + head/top view + language/context | left/right/head `6DoF` actions + gripper actions | 把 active perception 变成 action；对 robot head DoF 和 calibration 有要求 |
| [RDT2](../summaries/rdt2.md) | 大规模 enhanced UMI dataset；action chunks 已整理 | language, wrist RGB, continuous action chunks | 重点在模型 latency：RVQ、flow matching、distillation | language instruction + RGB observation | continuous action chunk；RVQ tokens；flow-matching action expert | 把 UMI data 扩展到 VLA；底层 raw sync 细节披露较少 |
| [HoMMI](../summaries/hommi.md) | 三 iPhone/ARKit 采集 wrist/head RGB-depth-pose-gripper trajectories | 2 wrist iPhones, 1 head iPhone, depth, 6DoF poses, gripper widths | ARKit shared frame；timestamped bridge；latency-corrected async inference | wrist 2D features + head 3D representation + proprioception | bimanual EE poses + 3D look-at point | 缓解移动操作全局上下文不足；3D representation 与 whole-body controller 更复杂 |
| [TAMEn](../summaries/tamen.md) | MoCap precision mode、VR portable mode、AR recovery mode | RGB, pose markers/VR, gripper state, optional tactile | structured marker object tracking；online feasibility validation | wrist RGB + optional tactile observations | 16D continuous joint/gripper actions | 面向 contact-rich/recovery；触觉是辅助 stream，MoCap/VR 模式各有 trade-off |
| [ARCap](../summaries/arcap.md) | Quest/Rokoko/D435 采集 hand/wrist/head/point-cloud data 并 retarget | point cloud, headset pose, glove/controller pose, virtual robot state | AR world frame；virtual/real robot base alignment；real-time warnings | colored point cloud latent + current joint angle | target robot joint angles / gripper open-close | 采集时暴露 robot constraints；joint-space data 对 embodiment 更绑定 |
| [exUMI](../summaries/exumi.md) | AR MoCap + rotary encoder + modular tactile sensing | AR pose, encoder/gripper state, RGB/tactile streams | tactile/encoder/pose calibration 到 device frame | visual/proprioceptive + tactile auxiliary observations | UMI-like control trajectory with tactile-aware objectives | 说明 UMI stack 可扩展到 tactile；触觉学习不是本专题主轴 |

## 3. 结论
第一，UMI 系列的 trajectory acquisition 从 fragile but integrated 的 GoPro VIO，逐步分化为更工程化的 tracking module、AR/VR shared frame、MoCap/VR dual mode 和 large-scale hardware redesign。不同路线的核心 trade-off 是 portability、precision、drift、calibration cost 和 robot executability。

第二，多传感器对齐不是单一问题。UMI/FastUMI 主要是 temporal latency 与 sampling-rate alignment；HoMMI/ActiveUMI 主要是 shared 3D/world frame 与 active perception alignment；TAMEn/ARCap 进一步把 robot feasibility/collision/speed constraints 前移到采集阶段。

第三，state/action 表征是 UMI 系列能否跨 embodiment 的中心设计。Relative EE trajectory、task-frame trajectory、gripper-centric 3D representation、look-at point 和 RVQ action tokens 都是在不同层面减少 robot-specific coupling。反过来，joint-space action 在 TAMEn/ARCap 中更直接可执行，但跨平台复用性较弱。

## 4. 证据来源
- 原始 UMI 与 UMI on Legs 的 policy interface 证据来自对应 Zotero PDF 与项目页。
- FastUMI 的 trajectory generation、ROS sync、ACT/DP adaptation 来自 Zotero PDF。
- ActiveUMI 的 head/controller tracking、zero-point calibration、active perception action 来自 Zotero PDF 和 arXiv `2510.01607`。
- RDT2 的 action chunk、RVQ、flow matching、distillation 来自 Zotero PDF、项目页和本地 `/Users/ruanyifan/code/RDT2`。
- HoMMI 的 ARKit shared frame、3D visual representation、look-at point 和 async bridge 来自 Zotero PDF 与本地 `/Users/ruanyifan/code/umi/hommi`。
- TAMEn、ARCap、exUMI 的附属证据来自对应 PDF/项目页和本地代码。

## 5. 潜在冲突或例外情况
- `RDT2` 项目页标题使用 "Enabling Zero-Shot Cross-Embodiment Generalization by Scaling Up UMI Data"，Zotero/arXiv 标题使用 "Exploring the Scaling Limit..."；wiki 以 arXiv/Zotero 标题为文献信息，项目页标题作为别名处理。
- `ActiveUMI` 的 Zotero metadata 缺 date/DOI；wiki 使用 arXiv `2510.01607` 补证。
- `TAMEn` 与 `exUMI` 的触觉内容很容易成为独立专题；本页只保留其作为 synchronized auxiliary stream 与 recovery signal 的角色。

## 6. 相关链接
- 概念页：[Robot-Free Trajectory Acquisition](../concepts/robot-free-trajectory-acquisition.md)
- 概念页：[Multi-Sensor Synchronization for Robot Data](../concepts/multi-sensor-synchronization-for-robot-data.md)
- 概念页：[State-Action Representation for UMI](../concepts/state-action-representation-for-umi.md)
- 概念页：[Cross-Embodiment Policy Interface](../concepts/cross-embodiment-policy-interface.md)
