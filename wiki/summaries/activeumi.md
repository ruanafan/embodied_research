---
tags: [EmbodiedAI, Robotics, UMI, Active_Perception, Robot_Free_Demonstration]
last_updated: 2026-05-03
source: [Zotero, Local, Web]
status: [Draft]
---

# ActiveUMI

## 文献信息
- Title: ActiveUMI: Robotic Manipulation with Active Perception from Robot-Free Human Demonstrations
- Authors: Qiyuan Zeng, Chengmeng Li, Jude St. John, Zhongyi Zhou, Junjie Wen, Guorui Feng, Yichen Zhu, Yi Xu
- Date: 2025-10-02
- DOI: `10.48550/arXiv.2510.01607`
- Zotero: `zotero://select/library/items/6KHENWU9`
- Local raw file: [paper.pdf](../../raw/activeumi_robotic_manipulation_with_active_perception_from_robot_free_human_demonstrations/paper.pdf)
- Project: [activeumi.github.io](https://activeumi.github.io/)
- Local code: not found under `/Users/ruanyifan/code/`; use Zotero PDF and project page as primary sources.

## 1. 研究问题
ActiveUMI 关注 wrist-camera-only UMI 在遮挡、长时程任务和需要主动看目标的操作中的不足：如果人类示范时的 head movement/visual attention 也被记录，能否让 robot policy 学会主动调整 viewpoint？来源：Zotero item `6KHENWU9`、arXiv `2510.01607`。

## 2. 核心贡献
- 使用 Meta Quest 3s HMD 与改装 VR controllers，构建 portable VR data collection kit。
- 将 target robot grippers 或其结构镜像到 VR controllers 上，减少 operator controller 与 robot end-effector 的 kinematic mismatch。
- 明确记录 head pose/head camera view，把 active egocentric perception 作为 policy 可学习的 action/observation 关系。
- 在 bimanual tasks 中比较 wrist-only UMI、fixed head camera、ActiveUMI，报告 ActiveUMI 在 in-distribution 与 novel environments 中更高成功率。来源：本地 PDF Sections 3-4 与项目页。

## 3. 轨迹数据获取
ActiveUMI 从 Quest headset 与 controllers 获取三个关键 6DoF pose：left controller/end-effector、right controller/end-effector、HMD/head。Quest inside-out tracking 同时跟踪 controller 与 head，在统一 world coordinate system 中记录 trajectory。controller 上还集成 gripper actuation motor，使 gripper open/close 与手持输入同步。来源：本地 PDF Sections 3.1/3.3。

它的 trajectory acquisition 与原始 UMI 不同：UMI 使用 gripper-mounted GoPro+IMU 恢复 EE pose，而 ActiveUMI 直接利用 VR tracking 得到 controller/head 6DoF trajectories；head trajectory 不只是辅助传感器，而是 active perception 行为标签。来源：本地 PDF Figure 3 与 Section 3.2。

## 4. 多传感器对齐
ActiveUMI 通过 HMD 建立统一 world coordinate system，同时 tracking head 与 controllers，因此核心对齐是 headset/controllers 到 robot kinematics 的 calibration。系统包含 in-situ environment setup、gripper placeholder 与 haptic feedback for zero-point position，使每次 collection session 以一致 zero-point 和 base coordinate 开始。来源：本地 PDF Section 3.3。

所有 sensor and robot data 以 `30Hz` 收集；dataset 中包含 language、joint/action labels、两路 wrist camera 和一路 top/head camera view。由于 head pose 与 controller poses 同源于 VR tracking，其 temporal alignment 比 UMI 的分布式 camera/proprioception latency matching 简化，但 precision 依赖 VR tracking quality 与 zero-point calibration。来源：本地 PDF Figure 3 与 Section 4.1。

## 5. State / Action 表征
ActiveUMI 的训练 observation 包含 wrist cameras、head/top camera 或 head-related input，以及 language instruction；action 包含 bimanual gripper/arm control 和 head 6DoF pose。论文图示将 action 标为 `6 DoF x 3` 加 gripper `1 DoF x 2`，即左右手和 head 都进入 action space。来源：本地 PDF Figure 3/Section 3.2。

这个设计的原因是让 policy 学到“看哪里”和“怎么动手”之间的耦合：部署时，policy 可以预测 robot head pose，让 low-level controller 调整 movable camera viewpoint，主动获取被遮挡或任务关键的信息。相比 fixed top camera，它把 perception choice 变成 action；相比 wrist-only UMI，它减少 wrist view 的局部性。来源：本地 PDF Section 3.2/4.2。

## 6. 局限性
- 6DoF head action 对 robot head embodiment 有要求；若机器人只有 2DoF neck，需要像 HoMMI 那样进一步 relaxed action representation。
- VR tracking 简化同步，但对 headset SLAM、controller visibility 和 initial calibration 依赖更强。
- ActiveUMI 的 Zotero metadata 缺 date/DOI，已用 arXiv `2510.01607` 和项目页补证，后续可回填 Zotero。

## 7. 相关页面
- 概念页：[Robot-Free Trajectory Acquisition](../concepts/robot-free-trajectory-acquisition.md)
- 概念页：[Multi-Sensor Synchronization for Robot Data](../concepts/multi-sensor-synchronization-for-robot-data.md)
- 概念页：[Cross-Embodiment Policy Interface](../concepts/cross-embodiment-policy-interface.md)
- 相关摘要：[HoMMI](hommi.md)
- 综合页：[UMI Series Data Interface Overview](../syntheses/umi-series-data-interface-overview.md)

