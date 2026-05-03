---
tags: [EmbodiedAI, Robotics, UMI, Mobile_Manipulation, Whole_Body_Control, Policy_Interface]
last_updated: 2026-05-03
source: [Zotero, Local, Web]
status: [Draft]
---

# UMI on Legs

## 文献信息
- Title: UMI on Legs: Making Manipulation Policies Mobile with Manipulation-Centric Whole-body Controllers
- Authors: Huy Ha, Yihuai Gao, Zipeng Fu, Jie Tan, Shuran Song
- Date: 2024-07-14
- DOI: `10.48550/arXiv.2407.10353`
- Zotero: `zotero://select/library/items/GEMUMHA7`
- Local raw file: [paper.pdf](../../raw/umi_on_legs_making_manipulation_policies_mobile_with_manipulation_centric_whole_body_controllers/paper.pdf)
- Project: [umi-on-legs.github.io](https://umi-on-legs.github.io/)
- Code: project page links to GitHub; no local clone found under `/Users/ruanyifan/code/`.

## 1. 研究问题
UMI on Legs 问的是：已经用 UMI 学到的 table-top visuomotor manipulation policy，能否通过一个 manipulation-centric whole-body controller 被零样本搬到 quadruped mobile manipulator 上？核心不在重新采集 mobile robot demonstrations，而在设计一个能连接高层 manipulation policy 与低层 legged WBC 的 trajectory interface。来源：Zotero item `GEMUMHA7`、项目页。

## 2. 核心贡献
- 将 real-world robot-free UMI demonstrations 与 simulation-trained robot-centric WBC 组合起来。
- 使用 task-frame end-effector trajectory 作为 manipulation policy 与 whole-body controller 的接口。
- WBC 在 simulation 中学 task-frame trajectory tracking，不需要模拟每个 manipulation task 的 object dynamics 或 reward。
- 展示将原始 UMI cup policy plug-and-play 到 quadruped system 的 zero-shot cross-embodiment deployment。来源：本地 PDF Abstract/Section 3。

## 3. 轨迹数据获取
高层 manipulation trajectories 仍来自 UMI-style hand-held gripper demonstrations：wrist-mounted camera 输入到 diffusion policy，policy 输出 future end-effector pose targets。UMI on Legs 自己新增的数据重点不是 object-level robot teleoperation，而是训练 WBC 的 trajectory tracking 数据：在 simulation 中采样/跟踪 UMI-style end-effector trajectories，让 quadruped arm/legs 学会把 task-frame EE target 实现出来。来源：本地 PDF Fig. 3 与 Section 3.1/3.2。

部署系统还用 iPhone/ARKit 做 robot body pose estimation，以支持 task-space tracking 和 world-frame stabilization。项目页说明 robot dog 上有 head GoPro 作为 policy observation，iPhone stream body pose；论文中也强调 iPhone 形式的 robust odometry 用于 in-the-wild task-space tracking。来源：本地 PDF Section 3.3，项目页。

## 4. 多传感器对齐
UMI on Legs 的对齐重点是异步双层控制，而不是把所有传感器塞进单一同步网络。高层 manipulation policy 低频运行，低层 WBC 以 50Hz 输出 joint position targets；task-frame EE trajectory 作为两层之间的时间化接口，使低频 policy 与高频 controller 可以处理不同 latency 与 update rates。来源：本地 PDF Section 3 与 Fig. 3。

其关键 alignment 是坐标系层面的：高层 policy 输出 camera-frame trajectory，系统将其变换到 task-space，再由 WBC 追踪。WBC 使用 task-frame 而非 body-frame tracking，是为了在 base 被扰动时仍保持 end-effector 相对任务环境稳定。来源：本地 PDF Fig. 4 与 Section 3.2。

## 5. State / Action 表征
高层 policy 的 observation 是 GoPro RGB，action 是 camera-frame end-effector trajectory。低层 WBC 的 observation 包括 18 个 joint positions/velocities、base orientation/angular velocity、previous action，以及 manipulation policy 预测的 EE trajectory。EE pose 用 3D position 和 6D rotation representation 表示；WBC 输出 arm/leg joint position targets。来源：本地 PDF Section 3.2。

这个 state/action split 的原因很清楚：高层 policy 只表达 task intention 与 manipulation trajectory，低层 WBC 处理 embodiment-specific dynamics、base compensation 和 joint-level execution。task-frame EE trajectory 既足够直观可由 UMI demonstrations 学到，又足够 expressive，可让 WBC 预见未来 movement，例如 tossing 前提前 brace。来源：本地 PDF Section 3.1/3.2。

## 6. 局限性
- policy 到 WBC 是 one-way communication，无法向 manipulation policy 反馈 reachability 或 whole-body limits。
- 当前接口主要追踪 gripper/end-effector，尚未自然扩展到 feet、body 和多 end-effector 全身协同。
- 任务成功依赖 WBC 对 task-frame trajectory 的 tracking 能力；高层 policy 若输出不可达 target，低层只能尽量补救。来源：项目页 Q&A 与本地 PDF discussion。

## 7. 相关页面
- 概念页：[Cross-Embodiment Policy Interface](../concepts/cross-embodiment-policy-interface.md)
- 概念页：[State-Action Representation for UMI](../concepts/state-action-representation-for-umi.md)
- 相关摘要：[Universal Manipulation Interface](universal-manipulation-interface.md)
- 综合页：[UMI Series Data Interface Overview](../syntheses/umi-series-data-interface-overview.md)

