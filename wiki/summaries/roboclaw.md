---
tags: [EmbodiedAI, Robotics, VLM, VLA, Agentic_Robotics, Long_Horizon]
last_updated: 2026-05-03
source: [Zotero, Local, Web]
status: [Draft]
---

# RoboClaw: An Agentic Framework for Scalable Long-Horizon Robotic Tasks

## 文献信息
- Title: RoboClaw: An Agentic Framework for Scalable Long-Horizon Robotic Tasks
- Authors: Ruiying Li, Yunlang Zhou, YuYao Zhu, Kylin Chen, Jingyuan Wang, Sukai Wang, Kongtao Hu, Minhui Yu, Bowen Jiang, Zhan Su, Jiayao Ma, Xin He, Yongjian Shen, Yang Yang, Guanghui Ren, Maoqing Yao, Wenhao Wang, Yao Mu
- Date: 2026-04-01
- DOI: `10.48550/arXiv.2603.11558`
- arXiv: `2603.11558`
- Zotero: `zotero://select/library/items/NJ3FHPK2`
- Zotero attachment: `ZS3WJD4Z`
- Local raw file: [paper.pdf](../../raw/roboclaw_an_agentic_framework_for_scalable_long_horizon_robotic_tasks/paper.pdf)

## 1. 研究问题
RoboClaw 关注的是：当 VLA systems 已经能执行短时程 language-conditioned manipulation 时，如何把真实机器人中的数据采集、policy learning、部署执行、失败恢复放进同一个长时程闭环，减少人工 reset 和 brittle multi-policy execution。来源：Zotero item `NJ3FHPK2`，abstract 与 Sections 1/3。

## 2. 核心贡献
1. 提出 RoboClaw，一个由 VLM 驱动的 agentic robotics framework，用同一个 agent loop 统一 data collection、policy learning 和 long-horizon task execution。
2. 提出 Entangled Action Pairs（EAP），将 forward manipulation behavior 与 inverse recovery/reset behavior 配成自复位采集循环，减少人工环境 reset。
3. 用 VLM meta-controller 结合 structured memory、skill library 和 MCP tools 动态调度 policy primitives，进行长序任务的运行时监控、重试、replanning 和 human escalation。
4. 在真实机器人长序 manipulation 任务中，论文报告相对 baseline 的 long-horizon success rate 提升 `25%`，human time investment 降低 `53.7%`。来源：Zotero item `NJ3FHPK2`，abstract、Figure 4 与 Sections 3/4。

## 3. 方法概述
RoboClaw 的核心不是把 VLM 和 VLA 融成一个端到端模型，而是把二者放进一个更高层的 agentic lifecycle：

1. **VLM meta-controller**：读取视觉观测和 structured memory，进行 in-context reasoning / CoT reasoning，判断当前 scene、subtask、success criteria 和下一步 tool call。
2. **Structured memory**：包含 role identity、task-level memory 和 working memory；task-level memory 记录 global task、decomposed subtasks 和执行状态，working memory 记录当前 skill 与 tool invocation history。
3. **Skills / Tools / Policies 三层抽象**：Skills 是可复用流程，Tools 是 MCP 可调用接口，Policies 是产生低层动作的 VLA models。
4. **EAP 数据采集**：对每个 policy `k` 学习 forward policy $\pi_{\theta_k}^{\rightarrow}$ 与 reset policy $\pi_{\phi_k}^{\leftarrow}$，形成 $(\tau_k^{\rightarrow}, \tau_k^{\leftarrow})$ pair，并把轨迹写入 dataset `D`。
5. **Deployment-time supervision**：执行时 agent 选择 policy、查询环境摘要与 robot status；若 success condition 不满足，则 retry、切换 policy、replan 或请求 human intervention。

来源：Zotero item `NJ3FHPK2`，Sections 3.1-3.3。

## 4. 实验设置
- 机器人平台：论文使用 Agibot G01 real-world manipulation setting。来源：Zotero item `NJ3FHPK2`，README 与实验描述。
- 长序评估任务：bedroom vanity table organization、kitchen shelf organization、study desk organization、convenience-store shelf retrieval。来源：本地代码仓 README 与论文实验部分。
- 单技能 policy 评估：body lotion placement、primer placement with drawer closing、lipstick insertion、tissue wipe。来源：Zotero item `NJ3FHPK2`，Section 4.2。
- Low-level policy：论文中底层 manipulation policies 使用 `π0.5` VLA，并通过 conditional flow matching 预测 action chunk $A_t = \pi_{0.5}(o_t, l_t, q_t)$。来源：Zotero item `NJ3FHPK2`，Section 3.2。
- Fine-tuning 设置：论文表 1 报告 `π0.5` fine-tuning 使用 LoRA rank `16`、batch size `16`、training steps `10k`、learning rate `2.5e-5` 等超参数。来源：Zotero item `NJ3FHPK2`，Table 1。

## 5. 关键指标或结果
- 对相同数据量，manual data collection baseline 需要约 `2.16x` human time。来源：Zotero item `NJ3FHPK2`，Figure 4(a) 与 Section 4.1。
- rollout execution 中，manual baseline 需要约 `8.04x` human intervention。来源：Zotero item `NJ3FHPK2`，Figure 4(b) 与 Section 4.1。
- inverse reset policies 在四个 manipulation tasks 上达到 `36/50` 到 `43/50` 的成功次数，支撑 EAP 自复位采集循环。来源：Zotero item `NJ3FHPK2`，Table 2 与 Section 4.2。
- 迭代 rollout 后，forward policies 成功率随 1 到 5 次 iteration 稳定提升，例如 body lotion 从 `21/50` 到 `43/50`，primer 从 `23/50` 到 `40/50`，lipstick insertion 从 `2/50` 到 `23/50`，tissue wipe 从 `11/50` 到 `26/50`。来源：Zotero item `NJ3FHPK2`，Table 3 与 Section 4.2。
- 在 vanity table organization 长序任务上，RoboClaw 相比 `π0.5` 同数据 baseline 和 product-of-subtask-success baseline 表现更好，论文将原因归因于 progress monitoring 与 automatic recovery policy invocation。来源：Zotero item `NJ3FHPK2`，Figure 4(c)、Figure 5 与 Section 4.3。

## 6. 为什么重要
RoboClaw 对本知识库中 VLM+VLA 长序任务讨论的意义在于：它把“VLM 输出子任务、VLA 执行动作”的接口扩展成了一个完整生命周期系统。它强调的不只是单次 inference 的 high-level planning，而是：
- 数据采集阶段就使用同一个 VLM agent 和 skill/tool semantics；
- policy training 依赖 forward/reverse rollout pairs 与 human intervention 后的失败恢复数据；
- 部署阶段复用相同 structured memory 与 tool/policy 调度逻辑；
- 失败模式被写回 policy library，逐步形成 recovery policies。

这使 RoboClaw 更像一个 VLM+VLA system operations layer，而不是一个独立替代 VLA 的模型。来源：Zotero item `NJ3FHPK2`，Sections 1/3/4。

## 7. 局限性
- 系统复杂度显著高于最小 VLM+VLA pipeline，需要 skill library、MCP tools、policy servers、run logs 和 reset policies。
- EAP 依赖可行的 inverse reset behavior；许多真实任务不一定存在稳定、低成本的 reverse action。
- 论文结论主要来自特定硬件平台、policy pool 与任务族，泛化到其他 embodiment 需要验证。
- 论文结论指出 cloud-based large models 可能引入 latency；这对高频交互或安全敏感任务是工程约束。来源：Zotero item `NJ3FHPK2`，Conclusion。

## 8. 本地代码来源
- Local repo: `/Users/ruanyifan/code/RoboClaw`
- Remote: `https://github.com/RoboClaw-Robotics/RoboClaw.git`
- Commit: `5238184185efee5c36017f10a79c2e0de4830690`
- 代码性质：论文关联开源仓库；arXiv 与 README 均指向该项目代码。
- 关键入口文件：
  - `/Users/ruanyifan/code/RoboClaw/README.md`
  - `/Users/ruanyifan/code/RoboClaw/src/agent_demo/agent_layer/agent_prompt/references/RoboClaw.md`
  - `/Users/ruanyifan/code/RoboClaw/skills/eap-data-collection/SKILL.md`
  - `/Users/ruanyifan/code/RoboClaw/skills/long-horizon-execution/SKILL.md`
  - `/Users/ruanyifan/code/RoboClaw/skills/monitored-subtask-execution/SKILL.md`
  - `/Users/ruanyifan/code/RoboClaw/src/mcp_server_demo/corobot_mcp_server/src/server.py`

本地代码显示，当前开源实现把 `eap-data-collection`、`long-horizon-execution` 和 `monitored-subtask-execution` 组织为 skill workflow；底层 `corobot_mcp_server` 的 `set_evaluate_params` 接收 `policy.host`、`policy.port`、`prompt` 和 `step_interval`，用于启动一次 prompt-driven PolicyTask。来源：本地 repo commit `5238184185efee5c36017f10a79c2e0de4830690`。

## 9. 来源与引用
- Zotero item: `NJ3FHPK2`
- Zotero attachment: `ZS3WJD4Z`
- DOI: `10.48550/arXiv.2603.11558`
- arXiv URL: `http://arxiv.org/abs/2603.11558`
- Local raw PDF: [paper.pdf](../../raw/roboclaw_an_agentic_framework_for_scalable_long_horizon_robotic_tasks/paper.pdf)
- Local code repo: `/Users/ruanyifan/code/RoboClaw`

## 10. 相关页面
- 综合页：[RoboClaw vs VLM+VLA Long-Horizon](../syntheses/roboclaw-vs-vlm-vla-long-horizon.md)
- 综合页：[VLA Data Annotation and Training](../syntheses/vla-data-annotation-and-training.md)
- 相关摘要：[π0.5](pi0-5.md)
- 相关摘要：[Hi Robot](hi-robot.md)
- 概念页：[Hierarchical Language Supervision for VLA](../concepts/hierarchical-language-supervision-for-vla.md)
