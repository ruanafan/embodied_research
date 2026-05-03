---
tags: [EmbodiedAI, Robotics, UMI, Mobile_Manipulation, Active_Perception, Policy_Interface]
last_updated: 2026-05-03
source: [Zotero, Local, Web]
status: [Draft]
---

# HoMMI

## 文献信息
- Title: HoMMI: Learning Whole-Body Mobile Manipulation from Human Demonstrations
- Authors: Xiaomeng Xu, Jisang Park, Han Zhang, Eric Cousineau, Aditya Bhat, Jose Barreiros, Dian Wang, Shuran Song
- Date: 2026-03-03
- DOI: `10.48550/arXiv.2603.03243`
- Zotero: `zotero://select/library/items/SZJPKIE4`
- Local raw file: [paper.pdf](../../raw/hommi_learning_whole_body_mobile_manipulation_from_human_demonstrations/paper.pdf)
- Project: [hommi-robot.github.io](https://hommi-robot.github.io/)
- Local code: `/Users/ruanyifan/code/umi/hommi`
  - Remote: `git@github.com:xxm19/hommi.git`
  - Commit: `796f24360b6ae4d89fb00da888705219254cd56b`
  - Key entry files: `hommi/demonstration_processing/process_demos_iphone.py`, `hommi/demonstration_processing/build_umi_dataset_iphone.py`, `hommi/train_network/train.py`, `hommi/deployment/policy_server.py`

## 1. 研究问题
HoMMI 处理的是 mobile manipulation 中 wrist-only UMI 的信息不足：机器人需要 navigation、bimanual coordination 和 active perception，仅 wrist camera 无法提供全局上下文。但直接加入 head-mounted egocentric view 会放大 human-to-robot visual/action embodiment gap。来源：Zotero item `SZJPKIE4`、项目页。

## 2. 核心贡献
- 在 UMI grippers 上加入 egocentric sensing，用三台 iPhone 采集 wrist/head RGB、depth、6DoF poses 和 gripper widths。
- 使用 ARKit multi-device collaboration 建立 shared coordinate frame。
- 提出 embodiment-agnostic 3D visual representation、3D look-at point head action、gripper-centric frame。
- 用 constraint-aware whole-body controller 将 hand-eye trajectories 转成 robot whole-body motions。来源：本地 PDF Sections IV-VI。

## 3. 轨迹数据获取
HoMMI 的 data collection interface 使用三台 iPhone：两台装在 grippers 上，一台装在 cap 上作为 head/egocentric sensor。每次 demonstration 以 `60Hz` 记录 RGB video、depth maps、6DoF poses 和 gripper widths，形成 synchronized multimodal trajectories。Apple ARKit multi-device collaboration 负责建立 shared coordinate frame。来源：本地 PDF Section IV。

相比 UMI，HoMMI 不只是采集 end-effector trajectories，还采集 head motion 与 egocentric observation；但训练时不直接要求机器人复制 human 6DoF head pose，而是把 head behavior 转成更可迁移的 look-at point。来源：本地 PDF Sections IV-V。

## 4. 多传感器对齐
采集阶段的核心对齐由 ARKit shared frame 完成：多个 iPhone 在同一个 globally consistent coordinate frame 中记录 wrist/head views 与 6DoF poses。处理阶段本地代码提供 `process_demos_iphone.py`、`create_session_iphone.py`、`build_umi_dataset_iphone.py`，将 raw sessions 组织为 dataset plan 与 `dataset.zarr.zip`。来源：本地代码 README 与本地 PDF Section IV。

部署阶段，HoMMI 采用 asynchronous policy inference：policy server 接收 timestamped observations，execution bridge 对 camera/proprioception 做 measured-latency correction，以 latest camera timestamp 为 anchor 插值 proprioception，并丢弃过期 actions。这个机制继承 UMI latency matching，但扩展到 mobile whole-body system。来源：本地 PDF Section VI-C。

## 5. State / Action 表征
HoMMI 的 observation embedding 包含 wrist 2D image features、head egocentric 3D visual representation 和 proprioception。head image 被切成 patches，每个 patch 绑定 pointmap 中的 3D point，并在 gripper frame 中 mask out arms/body points；这样可以缓解 human/robot torso、height、viewpoint 差异。来源：本地 PDF Section V-A。

action 包含 bimanual end-effector poses 与 head look-at point。look-at point 是 relaxed head action representation：训练时从 center camera ray 与 scene pointmap 的交点得到，推理时由 head controller 转成 robot feasible head orientation。所有 gripper poses、head pointmaps、look-at points 都转到 left-gripper-centric frame，使 observation/action 以执行器为中心而不是以人/机器人头部为中心。来源：本地 PDF Sections V-B/V-C。

## 6. 局限性
- 3D pointmap/egocentric representation 增加 processing pipeline 复杂度。
- look-at point 能缓解 6DoF head pose gap，但仍依赖 robot head/neck 能够覆盖任务相关视角。
- whole-body IK/controller 需要在 tracking accuracy、smoothness、stability、自碰撞和 CoM constraints 之间权衡。来源：本地 PDF Section VI-B。

## 7. 相关页面
- 概念页：[Multi-Sensor Synchronization for Robot Data](../concepts/multi-sensor-synchronization-for-robot-data.md)
- 概念页：[State-Action Representation for UMI](../concepts/state-action-representation-for-umi.md)
- 概念页：[Cross-Embodiment Policy Interface](../concepts/cross-embodiment-policy-interface.md)
- 相关摘要：[ActiveUMI](activeumi.md)
- 综合页：[UMI Series Data Interface Overview](../syntheses/umi-series-data-interface-overview.md)

