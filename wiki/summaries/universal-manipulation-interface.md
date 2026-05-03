---
tags: [EmbodiedAI, Robotics, UMI, Robot_Free_Demonstration, Policy_Interface]
last_updated: 2026-05-03
source: [Zotero, Local, Web]
status: [Draft]
---

# Universal Manipulation Interface

## 文献信息
- Title: Universal Manipulation Interface: In-The-Wild Robot Teaching Without In-The-Wild Robots
- Authors: Cheng Chi, Zhenjia Xu, Chuer Pan, Eric Cousineau, Benjamin Burchfiel, Siyuan Feng, Russ Tedrake, Shuran Song
- Date: 2024-03-06
- DOI: `10.48550/arXiv.2402.10329`
- Zotero: `zotero://select/library/items/35K3GMHY`
- Local raw file: [paper.pdf](../../raw/universal_manipulation_interface_in_the_wild_robot_teaching_without_in_the_wild_robots/paper.pdf)
- Project: [umi-gripper.github.io](https://umi-gripper.github.io/)
- Local code: `/Users/ruanyifan/code/umi/universal_manipulation_interface`
  - Remote: `https://github.com/real-stanford/universal_manipulation_interface.git`
  - Commit: `8ea6ba767a981be8d7b3be84f1bdbd74dbf2c2ed`
  - Key entry files: `run_slam_pipeline.py`, `train.py`, `eval_real.py`, `diffusion_policy/config/train_diffusion_unet_timm_umi_workspace.yaml`

## 1. 研究问题
UMI 试图回答：不在真实机器人上 teleoperation，能否直接用手持 gripper 在真实环境中采集可迁移到机器人 policy 的 manipulation demonstrations？关键挑战不是单纯采集视频，而是同时让 observation、action、latency 和 embodiment interface 在训练与部署时足够一致。来源：Zotero item `35K3GMHY` 与本地 PDF。

## 2. 核心贡献
- 提出手持 UMI gripper，用 wrist-mounted GoPro、fisheye view、side mirrors 和 IMU-aware tracking 采集 in-the-wild demonstrations。
- 设计可部署的 policy interface：latency matching、relative trajectory action representation、relative proprioception。
- 通过 shared gripper/camera geometry 降低 human demonstration 与 robot deployment 的 observation/action embodiment gap。
- 支持 dynamic、bimanual、precise、long-horizon tasks，并通过 changing data 而非重新设计 task pipeline 来学习新技能。来源：Zotero item `35K3GMHY`、项目页。

## 3. 轨迹数据获取
UMI 的核心轨迹来自 GoPro 视频中的 visual-inertial tracking。GoPro 同时记录 RGB 与 IMU，系统用 IMU-aware monocular tracking 恢复 hand-held gripper 的 6DoF pose；gripper width 通过 gripper 上的 fiducial markers 连续估计。对每个 scene，UMI 先建立 scene-level map，再将 demonstration relocalize 到同一 map 中，因此 bimanual 数据可以计算 inter-gripper relative pose。来源：本地 PDF Sections III-A/III-B。

轨迹不是直接以 robot joint labels 采集，而是以 end-effector pose 与 gripper width 采集，再经过 embodiment-specific kinematic filtering 选择目标机器人可达的 trajectories。这个设计让同一份 robot-free demonstration 可以被不同 robot embodiments 复用，但也把精度瓶颈放在 SLAM/VIO、camera-gripper geometry 和 filtering 上。来源：本地 PDF HD4/HD5/HD6。

## 4. 多传感器对齐
UMI 区分两类延迟：observation latency 与 action execution latency。部署时，RGB image、robot EE pose 和 gripper width 来自不同硬件，系统先测量每条 observation stream 的 latency，再以最高 latency stream 通常是 camera 为锚点，对 proprioception/gripper streams 做 temporal interpolation。bimanual cameras 通过 nearest-neighbor frame 做 soft synchronization。来源：本地 PDF Fig. 5 与 PD1.1。

action side 则使用 action latency matching：policy 输出带 desired timestamp 的 future EE poses/gripper widths；系统丢弃已过期动作，并提前发送仍可执行的 action commands，以补偿 inference latency 和 robot/gripper execution latency。这个设计是 dynamic tossing 等高速任务能够部署的关键。来源：本地 PDF PD1.2。

## 5. State / Action 表征
UMI 的 policy state/observation 包含 synchronized RGB images、history relative EE pose 和 gripper width。action 是一个 horizon 的 desired relative EE pose 与 gripper width。论文明确比较了 absolute action、delta action 与 relative trajectory：absolute action 需要全局坐标定义，delta action 容易累积误差，而 relative trajectory 表示从当前 EE pose 出发的一串未来 SE(3) targets，兼顾跨环境泛化与低误差执行。来源：本地 PDF Fig. 5/6 与 PD2。

这里的 `state` 更接近 robot learning 中的 observation/proprioception/history context，而不是完整 Markov state。UMI 选择 relative proprioception 还有一个 practical reason：当 observation horizon 为 2 时，history relative pose 提供速度信息，同时避免依赖 robot-specific joints 或 robot base placement。来源：本地 PDF PD2.2。

## 6. 局限性
- GoPro/VIO/SLAM 仍是脆弱环节，低纹理、运动模糊或环境变化会影响 pose recovery。
- latency matching 需要每个部署硬件测量 camera、inference、arm、gripper 延迟；工程复杂度不可忽略。
- relative EE trajectory 有利于跨 embodiment，但无法表达所有 robot-specific constraints，需要 kinematic filtering 或 lower-level controller 承接。

## 7. 相关页面
- 概念页：[Robot-Free Trajectory Acquisition](../concepts/robot-free-trajectory-acquisition.md)
- 概念页：[Multi-Sensor Synchronization for Robot Data](../concepts/multi-sensor-synchronization-for-robot-data.md)
- 概念页：[State-Action Representation for UMI](../concepts/state-action-representation-for-umi.md)
- 综合页：[UMI Series Data Interface Overview](../syntheses/umi-series-data-interface-overview.md)

