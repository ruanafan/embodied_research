---
tags: [EmbodiedAI, Robotics, UMI, Policy_Interface, Action_Representation]
last_updated: 2026-05-03
source: [Zotero, Local, Web]
status: [Draft]
---

# State-Action Representation for UMI

## 1. 定义
UMI 系列中的 state/action representation 指训练 policy 时如何把 raw sensor streams 映射为 observation/proprioception/history context，以及如何把 human demonstrations 映射为 action labels。这里的 `state` 通常不是完整 Markov state，而是 RGB/depth/head view、relative pose、gripper width、joint state、language instruction 等 policy 可见输入。来源：[Universal Manipulation Interface](../summaries/universal-manipulation-interface.md)、[RDT2](../summaries/rdt2.md)。

## 2. 在具身智能中的作用
表征决定了数据能否跨 embodiment、跨场景、跨模型架构复用。UMI 的 relative EE trajectory 去掉 global frame 依赖；UMI on Legs 的 task-frame trajectory 把 manipulation policy 与 WBC 解耦；RDT2 的 RVQ/flow matching 将 UMI action chunks 接入大 VLM；HoMMI 的 gripper-centric 3D representation 减小 head/torso embodiment gap。来源：对应摘要页。

## 3. 相关方法或代表性范式
- Relative EE trajectory：从当前 EE pose 出发的未来 SE(3) target sequence，避免 absolute frame 依赖与 delta error accumulation。
- Task-frame EE trajectory：高层 manipulation policy 输出 trajectory，低层 WBC 负责 embodiment-specific tracking。
- Joint trajectory：对某一 robot embodiment 直接，可执行性强，但跨平台弱。
- TCP pose trajectory：比 joint action 更 platform-independent，需要 IK 或 controller 映射。
- Action chunk/token：RDT2 中连续 action chunk 可被 RVQ 离散化为 action tokens，也可由 flow-matching action expert 直接连续生成。
- Look-at point：HoMMI 用 3D point 表达 active perception intent，避免直接回归 human 6DoF head pose。来源：[UMI on Legs](../summaries/umi-on-legs.md)、[HoMMI](../summaries/hommi.md)、[FastUMI](../summaries/fastumi.md)。

## 4. 相关论文
- [Universal Manipulation Interface](../summaries/universal-manipulation-interface.md)
- [UMI on Legs](../summaries/umi-on-legs.md)
- [FastUMI](../summaries/fastumi.md)
- [RDT2](../summaries/rdt2.md)
- [HoMMI](../summaries/hommi.md)
- [ActiveUMI](../summaries/activeumi.md)

## 5. 相关概念链接
- [Robot-Free Trajectory Acquisition](robot-free-trajectory-acquisition.md)
- [Multi-Sensor Synchronization for Robot Data](multi-sensor-synchronization-for-robot-data.md)
- [Cross-Embodiment Policy Interface](cross-embodiment-policy-interface.md)

## 6. 争议点或开放问题
- Absolute actions 更接近 robot execution，但对 global frame 和 robot setup 敏感。
- Relative actions 更可迁移，但可能隐藏 reachability/force/whole-body constraints。
- Large VLA 需要高压缩、高吞吐 action representation；小型 diffusion policy 可直接预测 continuous trajectories，但扩展到 open-vocabulary tasks 时语言/视觉对齐能力不足。

