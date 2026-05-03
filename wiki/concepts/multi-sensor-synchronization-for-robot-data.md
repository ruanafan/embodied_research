---
tags: [EmbodiedAI, Robotics, UMI, Sensor_Fusion, Data_Collection]
last_updated: 2026-05-03
source: [Zotero, Local, Web]
status: [Draft]
---

# Multi-Sensor Synchronization for Robot Data

## 1. 定义
机器人数据中的多传感器对齐（multi-sensor synchronization）指把不同频率、不同 latency、不同坐标系的 RGB/depth/pose/proprioception/gripper/head/tactile streams 变成同一时刻、同一参考系下的 policy observation/action labels。UMI 系列里，这通常同时包含 temporal synchronization、latency compensation 和 coordinate-frame alignment。来源：[Universal Manipulation Interface](../summaries/universal-manipulation-interface.md)、[FastUMI](../summaries/fastumi.md)、[HoMMI](../summaries/hommi.md)。

## 2. 在具身智能中的作用
如果多 sensor stream 未对齐，policy 会看到 out-of-sync state/action pairs，尤其在 dynamic tasks、bimanual manipulation 和 active perception 中会直接导致错误 actions。UMI 将 latency matching 视为 deployable policy interface 的核心；HoMMI 和 ActiveUMI 则通过 shared AR/VR frames 简化多视角同步；FastUMI 用 ROS clock/buffer/sub-sampling 把 GoPro 与 T265 合并。来源：对应摘要页。

## 3. 相关方法或代表性范式
- Latency matching：测量 camera/proprioception/gripper latency，以最慢 stream 为 anchor，插值其他 streams；action side 提前发送 commands。
- Unified clock + buffering：FastUMI 用 ROS unified clock 和 thread-safe queues，再做 synchronized sub-sampling。
- Shared AR/VR frame：HoMMI 用 ARKit multi-device collaboration，ActiveUMI 用 Quest headset/controllers world frame。
- Structured object tracking：TAMEn 用 marker topology 和 identity repair 解决 marker occlusion。
- Acquisition-time validation：ARCap/TAMEn 在采集时就检查 collision、speed、IK/reachability/execution constraints。来源：[ARCap](../summaries/arcap.md)、[TAMEn](../summaries/tamen.md)。

## 4. 相关论文
- [Universal Manipulation Interface](../summaries/universal-manipulation-interface.md)
- [FastUMI](../summaries/fastumi.md)
- [ActiveUMI](../summaries/activeumi.md)
- [HoMMI](../summaries/hommi.md)
- [TAMEn](../summaries/tamen.md)
- [exUMI](../summaries/exumi.md)

## 5. 相关概念链接
- [Robot-Free Trajectory Acquisition](robot-free-trajectory-acquisition.md)
- [State-Action Representation for UMI](state-action-representation-for-umi.md)
- [Cross-Embodiment Policy Interface](cross-embodiment-policy-interface.md)

## 6. 争议点或开放问题
- hardware synchronized data 不等于 deployment synchronized data；真实 robot 还会有 camera streaming、inference、controller、gripper execution latency。
- shared coordinate frame 可简化空间对齐，但可能把误差集中到 initial calibration 或 SLAM drift。
- 采集时 validation 能提高 replayability，但也可能限制 demonstrations 的自然性，需要在 scalability 与 executability 之间权衡。

