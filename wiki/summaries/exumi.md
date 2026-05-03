---
tags: [EmbodiedAI, Robotics, UMI, Tactile_Sensing, Data_Collection]
last_updated: 2026-05-03
source: [Local, Web]
status: [Draft]
---

# exUMI

## 文献信息
- Title: exUMI: Extensible Robot Teaching System with Action-aware Task-agnostic Tactile Representation
- Authors: Yue Xu, Litao Wei, Pengyu An, Qingyu Zhang, Yong-Lu Li
- Date: 2025-09-18
- DOI: `10.48550/arXiv.2509.14688`
- Local raw file: [paper.pdf](../../raw/exumi_extensible_robot_teaching_system_with_action_aware_task_agnostic_tactile_representation/paper.pdf)
- Web: [arXiv](https://arxiv.org/abs/2509.14688), [PMLR](https://proceedings.mlr.press/v305/xu25e.html), [project page](https://silicx.github.io/exUMI/)
- Local code: `/Users/ruanyifan/code/umi/exUMI`
  - Remote: `https://github.com/silicx/exUMI.git`
  - Commit: `2e6e64d67656aaf31b1a2a3ba236ddec4bd5e48a`
  - Key entry files: `README.md`, `DATA_COLLECTION.md`, `ARCap/calibrate_as5600.py`, `9DTact/shape_reconstruction/run_calibration.sh`
- Related local AR app fork: `/Users/ruanyifan/code/umi/exUMI-arcap`
  - Remote: `https://github.com/silicx/exUMI.git`
  - Commit: `21dae86bbb9137c78bbf8922827750cb7d2ec5eb`

## 1. 研究问题
exUMI 扩展原始 UMI 到 tactile-aware robot learning。本专题不展开 TPP/触觉表征本身，而关注它对 UMI data interface 的补充：如何通过 AR MoCap、rotary encoder、modular visuo-tactile sensing 和 automated calibration 提升 robot-free trajectory 数据可用性。来源：arXiv `2509.14688`、PMLR 页面、本地 README。

## 2. 核心贡献
- 在 vanilla UMI 上增加 robust proprioception：AR MoCap 与 rotary encoder。
- 设计 modular visuo-tactile sensing，使 tactile stream 能作为同步 auxiliary observation 接入。
- 提出 automated calibration，并报告 `100% data usability`。
- 用超过 `1M` tactile frames 训练 Tactile Prediction Pretraining，但本专题仅记录其作为辅助 sensor stream 的位置。来源：PMLR abstract 与本地 README。

## 3. 轨迹数据获取
exUMI 的 pose acquisition 依赖 ARCap/AR MoCap 获取 gripper 6D pose，并用 AS5600 rotary encoder/marker 等方式补充 gripper state。README 显示数据采集需要 Meta Quest ARCap APK、RaspberryPi/OrangePi、tactile sensors、AS5600 encoder calibration，并将 task-specific dataset 与 UMI-Data 项目关联。来源：本地 README 与 `DATA_COLLECTION.md`。

与 FastUMI/TAMEn 类似，exUMI 的关键变化是把原始 UMI 的 fragile VIO/SLAM pressure 转移到更明确的 proprioception/tracking/calibration modules，同时允许插入 tactile sensor。来源：arXiv abstract 与本地 README。

## 4. 多传感器对齐
exUMI 的对齐对象包括 AR pose、encoder/gripper state、tactile camera stream 和 RGB observation。README 中的 setup 流程包含 tactile camera calibration、AS5600 calibration 与 ARCap 6D pose mocap；这些步骤共同保证各 stream 能被解释到同一 gripper/device frame。来源：本地 README。

由于 exUMI 侧重触觉，本专题只把 tactile stream 记为 synchronized auxiliary observation。它的知识价值在于：UMI-like interface 一旦加入非视觉传感器，对齐问题会从 image-pose synchronization 扩展到 tactile image/shape reconstruction、encoder state 和 gripper pose 的共同标定。来源：PMLR abstract、本地 README。

## 5. State / Action 表征
exUMI 的 state/observation 包含 UMI-style visual/proprioceptive data 和 tactile observations；action 仍围绕 task execution 的 robot/gripper control trajectory。论文的独立重点是 action-aware temporal tactile prediction，即用 action context 预测 tactile dynamics，缓解 tactile sparsity。来源：arXiv abstract、PMLR abstract。

在本专题的 taxonomy 中，exUMI 不作为主 action representation 方案，而作为“UMI interface 可扩展 sensor stack”的例子：当 state 中加入 tactile stream 时，action 不一定改变，但训练目标可以增加 auxiliary representation learning。来源：PMLR abstract。

## 6. 局限性
- 本地 Zotero 未检索到 exUMI 条目，当前来源为 Web/PMLR、arXiv PDF 与本地代码。
- 触觉模块虽重要，但对用户当前问题是次要信息；本页避免把 TPP 细节展开成主线。
- 多传感器同步与 calibration 细节需要后续直接读 `DATA_COLLECTION.md` 和 scripts 做更细工程审计。

## 7. 相关页面
- 概念页：[Multi-Sensor Synchronization for Robot Data](../concepts/multi-sensor-synchronization-for-robot-data.md)
- 概念页：[Robot-Free Trajectory Acquisition](../concepts/robot-free-trajectory-acquisition.md)
- 相关摘要：[ARCap](arcap.md)
- 相关摘要：[TAMEn](tamen.md)
- 综合页：[UMI Series Data Interface Overview](../syntheses/umi-series-data-interface-overview.md)

