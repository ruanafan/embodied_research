---
tags: [EmbodiedAI, Robotics, UMI, Data_Collection, Robot_Free_Demonstration]
last_updated: 2026-05-03
source: [Zotero, Local, Web]
status: [Draft]
---

# Robot-Free Trajectory Acquisition

## 1. 定义
Robot-free trajectory acquisition 指不依赖真实目标机器人 teleoperation，而用手持 gripper、AR/VR controller、wearable interface 或 mobile sensing rig 直接采集可转换为 robot policy labels 的 human demonstration trajectories。它不是普通 human video learning，因为系统通常会同步记录 6DoF pose、gripper state、proprioception 或 retargeted robot state。来源：[Universal Manipulation Interface](../summaries/universal-manipulation-interface.md)、[FastUMI](../summaries/fastumi.md)、[ARCap](../summaries/arcap.md)。

## 2. 在具身智能中的作用
它的价值是把 robot data bottleneck 从“每个任务都用昂贵机器人采集”变成“用可分发的 interface 在真实场景收集 action-aligned trajectories”。UMI 与 RDT2 表明，如果 interface 本身足够 embodiment-agnostic，robot-free data 可以成为 cross-embodiment policy 或 VLA pretraining 的核心数据源。来源：[Universal Manipulation Interface](../summaries/universal-manipulation-interface.md)、[RDT2](../summaries/rdt2.md)。

## 3. 相关方法或代表性范式
- UMI：GoPro RGB/IMU + SLAM/VIO + gripper markers，得到 relative EE trajectory 和 gripper width。
- FastUMI：GoPro observation + T265 pose tracking + ArUco gripper width，派生 absolute TCP、relative TCP 和 joint trajectories。
- ActiveUMI：Quest headset/controllers 同时记录 left/right gripper 和 head 6DoF trajectories。
- HoMMI：三台 iPhone/ARKit 在 shared frame 中记录 wrist/head RGB、depth、pose 和 gripper width。
- TAMEn：MoCap precision mode 与 VR portable mode 双路径采集，并在采集时检查 robot executability。
- ARCap：采集 hand/wrist/head/point cloud，并实时 retarget 到 virtual robot 以暴露不可执行动作。来源：对应摘要页。

## 4. 相关论文
- [Universal Manipulation Interface](../summaries/universal-manipulation-interface.md)
- [UMI on Legs](../summaries/umi-on-legs.md)
- [FastUMI](../summaries/fastumi.md)
- [ActiveUMI](../summaries/activeumi.md)
- [HoMMI](../summaries/hommi.md)
- [TAMEn](../summaries/tamen.md)
- [ARCap](../summaries/arcap.md)

## 5. 相关概念链接
- [Multi-Sensor Synchronization for Robot Data](multi-sensor-synchronization-for-robot-data.md)
- [State-Action Representation for UMI](state-action-representation-for-umi.md)
- [Cross-Embodiment Policy Interface](cross-embodiment-policy-interface.md)

## 6. 争议点或开放问题
- 轨迹来源越便携，通常越需要处理 drift、tracking confidence、zero-point calibration 或 feasibility validation。
- robot-free data 的 action labels 并不天然 robot-executable；UMI 用 relative EE + filtering，ARCap/TAMEn 用采集时 validation，FastUMI 用 IK/joint trajectory conversion。
- 当任务需要 force/tactile/contact-rich feedback 时，robot-free trajectories 可能需要 recovery data 或 auxiliary sensing 才能覆盖失败边界。

