---
tags: [EmbodiedAI, Robotics, UMI, Cross_Embodiment, Policy_Interface]
last_updated: 2026-05-03
source: [Zotero, Local, Web]
status: [Draft]
---

# Cross-Embodiment Policy Interface

## 1. 定义
跨 embodiment policy interface 是一种中间层设计：policy 不直接输出某个机器人专属 joints/body commands，而输出更接近任务语义与 end-effector intention 的接口，例如 relative EE trajectory、task-frame trajectory、TCP pose、look-at point 或 action chunk。下游 robot-specific controller/IK/WBC 再把接口映射为具体 robot actions。来源：[Universal Manipulation Interface](../summaries/universal-manipulation-interface.md)、[UMI on Legs](../summaries/umi-on-legs.md)。

## 2. 在具身智能中的作用
它让 robot-free demonstrations 可以跨 robot arm、mobile base、head/neck geometry 或 gripper variant 复用。UMI 用 shared gripper/camera geometry 降低 observation/action gap；UMI on Legs 用 task-frame trajectory 接 quadruped WBC；HoMMI 用 gripper-centric frame 和 look-at point 缓解 egocentric embodiment gap；RDT2 用规模化 UMI action chunks 支撑 zero-shot cross-embodiment VLA。来源：对应摘要页。

## 3. 相关方法或代表性范式
- Hardware-level alignment：让 handheld device 与 robot-mounted device 使用相似 gripper/finger/camera geometry。
- Representation-level alignment：用 relative/gripper-centric/task-frame pose，而不是 robot base frame 或 joint space。
- Controller-level alignment：用 IK、whole-body controller 或 policy bridge 把 abstract trajectory 变成 robot-native commands。
- Acquisition-time alignment：ARCap/TAMEn 在采集阶段就可视化或检查 robot constraints，降低后续 retargeting failure。来源：[FastUMI](../summaries/fastumi.md)、[ARCap](../summaries/arcap.md)、[TAMEn](../summaries/tamen.md)。

## 4. 相关论文
- [Universal Manipulation Interface](../summaries/universal-manipulation-interface.md)
- [UMI on Legs](../summaries/umi-on-legs.md)
- [RDT2](../summaries/rdt2.md)
- [HoMMI](../summaries/hommi.md)
- [ARCap](../summaries/arcap.md)

## 5. 相关概念链接
- [Robot-Free Trajectory Acquisition](robot-free-trajectory-acquisition.md)
- [Multi-Sensor Synchronization for Robot Data](multi-sensor-synchronization-for-robot-data.md)
- [State-Action Representation for UMI](state-action-representation-for-umi.md)

## 6. 争议点或开放问题
- 越抽象的 interface 越容易跨 embodiment，但也越可能丢失 robot-specific constraints。
- lower-level controller 的能力上限会限制高层 policy 的可迁移性；例如 UMI on Legs 中不可达 trajectory 仍可能失败。
- 采集时引入 robot constraints 可提高 executability，但会削弱“完全 robot-free、自然示范”的自由度。

