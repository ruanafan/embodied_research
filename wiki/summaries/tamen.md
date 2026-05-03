---
tags: [EmbodiedAI, Robotics, UMI, Data_Collection, Contact_Rich_Manipulation, Policy_Interface]
last_updated: 2026-05-03
source: [Zotero, Local, Web]
status: [Draft]
---

# TAMEn

## 文献信息
- Title: TAMEn: Tactile-Aware Manipulation Engine for Closed-Loop Data Collection in Contact-Rich Tasks
- Authors: Longyan Wu, Jieji Ren, Chenghang Jiang, Junxi Zhou, Shijia Peng, Ran Huang, Guoying Gu, Li Chen, Hongyang Li
- Date: 2026-04-08
- DOI: `10.48550/arXiv.2604.07335`
- Zotero: `zotero://select/library/items/C344ARR7`
- Local raw file: [paper.pdf](../../raw/tamen_tactile_aware_manipulation_engine_for_closed_loop_data_collection_in_contact_rich_tasks/paper.pdf)
- Project: [opendrivelab.com/TAMEn](https://opendrivelab.com/TAMEn)
- Local code: `/Users/ruanyifan/code/umi/TAMEn`
  - Remote: `https://github.com/OpenDriveLab/TAMEn.git`
  - Commit: `4eccf9c1b35744cfd2c16d40a0c673c303854688`
  - Key entry files: `tAmeR/tAmeR_ws.py`, `src/vr_data_pub/vr_data_pub/vr_data_pub.py`, `src/vr_data_pub/vr_data_pub/teleoperation_control_30degree_xy.py`, `src/vr_data_pub/launch/teleoperation_system_30degree_xy.launch.py`

## 1. 研究问题
TAMEn 属于 UMI-style handheld paradigm 的 contact-rich/bimanual 扩展，但本专题只关注其数据工程侧：如何在精度、便携性、可执行性验证和 recovery data 之间组织 acquisition pipeline。触觉/力觉在这里作为额外 sensor stream 与 recovery signal 记录，不作为主线。来源：Zotero item `C344ARR7`、项目页。

## 2. 核心贡献
- 设计 cross-morphology wearable interface，可快速适配 heterogeneous grippers。
- 提出 dual-mode acquisition：precision mode 用 MoCap，portable mode 用 VR tracking 支持 in-the-wild acquisition 与 recovery。
- 在采集时进行 online feasibility checking，使 demonstrations 更可 replay 到 robot。
- 用 tAmeR AR teleoperation 在 policy execution failure 附近收集 recovery trajectories。来源：本地 PDF Abstract/Sections III-C/E。

## 3. 轨迹数据获取
TAMEn 的 nominal trajectories 可来自两种模式：precision mode 使用 motion capture markers 获取 sub-millimeter gripper pose；portable mode 将 marker assembly 替换为 quick-detachable VR handle，用 VR-based tracking 支持 in-the-wild collection。系统还通过 gripper mechanism/markers 记录 gripper opening 与 finger motion。来源：本地 PDF Fig. 2/Section III。

在 recovery mode 中，tAmeR 通过 AR headset 与 teleoperation programs 在 robot policy 失败或将失败时收集 corrective trajectories。这样 top-level recovery data 来自 policy-induced failure state distribution，而不是离线人工想象失败情形。来源：本地 PDF Sections III-B/III-E 与本地 README。

## 4. 多传感器对齐
TAMEn 的关键对齐问题是 bimanual contact-rich tasks 中 marker occlusion。论文将每个 handheld interface 表示为 structured marker object，利用 predefined topology 和 marker identities 做 pose estimation 与 marker recovery；先用短 unlabeled sequence 初始化 object model，再用 correction-based tracking 传播 marker identity，并局部修复 occlusion/ambiguity segment。来源：本地 PDF Section III-C。

在线可执行性验证也是一种 alignment：采集时将 recorded gripper poses 同步映射到 target robot poses，并检查 IK failure、soft limit violation、overspeed motion 和 runtime communication anomalies。它把 robot execution constraints 提前并入 acquisition loop，而不是事后 replay filtering。来源：本地 PDF Section III-C。

## 5. State / Action 表征
TAMEn downstream policy 以两路 wrist-mounted fisheye RGB observations 和可选 tactile observations 为输入，输出 `16-dimensional action`：两只 7DoF arms 的 joint commands 加两个 continuous gripper actions。触觉分支用于 contact-rich robustness，但本专题将其视作 synchronized auxiliary observation。来源：本地 PDF Section III-E。

这个 action 表征偏 robot-native joint/action space，而不是 UMI 的 relative EE trajectory。原因是 TAMEn 面向 bimanual contact-rich manipulation 与 recovery refinement，论文强调 closed-loop feasibility、robot execution constraints 和 DAgger-style recovery update；joint-level continuous action 更直接接入 target dual-arm platform。来源：本地 PDF Sections III-C/E。

## 6. 局限性
- MoCap precision mode 精度高但依赖外部设施；VR portable mode 便携但精度和 drift 需要额外验证。
- 触觉 stream 对 contact-rich tasks 有价值，但会增加同步、标定、数据规模与模型分支复杂度。
- 当前 open-source README 显示部分 hardware/data/training scripts 仍处 staged release，wiki 中相关工程结论应标记为待持续更新。来源：本地 README 与项目页。

## 7. 相关页面
- 概念页：[Robot-Free Trajectory Acquisition](../concepts/robot-free-trajectory-acquisition.md)
- 概念页：[Multi-Sensor Synchronization for Robot Data](../concepts/multi-sensor-synchronization-for-robot-data.md)
- 概念页：[State-Action Representation for UMI](../concepts/state-action-representation-for-umi.md)
- 相关摘要：[exUMI](exumi.md)
- 综合页：[UMI Series Data Interface Overview](../syntheses/umi-series-data-interface-overview.md)

