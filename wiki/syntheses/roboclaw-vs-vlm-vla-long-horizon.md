---
tags: [EmbodiedAI, Robotics, VLM, VLA, Agentic_Robotics, Long_Horizon, Comparative_Analysis]
last_updated: 2026-05-03
source: [Zotero, Local]
status: [Draft]
---

# RoboClaw 与 VLM+VLA 长序任务方案对比

## 1. 问题背景
本页比较两种容易混在一起的方案：

1. **VLM+VLA 分层方案**：VLM 将用户目标、图像、历史和 correction 转换为 `next_subtask`；VLA 将图像、proprioception 和 subtask 转换为 `action_chunk`。这是 [VLA Data Annotation and Training](vla-data-annotation-and-training.md) 中整理的最小可落地接口。
2. **RoboClaw-style agentic lifecycle framework**：VLM agent 不只输出 subtask，而是作为 meta-controller，在 data collection、policy learning 和 deployment 中统一调度 skills、tools 和 policy primitives。来源：[RoboClaw](../summaries/roboclaw.md)。

核心区别是：**VLM+VLA 主要解决“如何从语义到动作”，RoboClaw 主要解决“如何把采集、训练、部署、恢复放进同一个闭环”**。因此 RoboClaw 不是 VLM+VLA 的同层替代，而是更重的系统层扩展。

## 2. 接口与系统层级对比

| 维度     | VLM+VLA 分层方案                                  | RoboClaw                                                                  |
| ------ | --------------------------------------------- | ------------------------------------------------------------------------- |
| 系统定位   | 模型接口和数据标注方案                                   | Agentic robotics framework / lifecycle layer                              |
| 高层模块   | VLM planner / semantic policy                 | VLM meta-controller with structured memory                                |
| 低层模块   | VLA action policy                             | VLA/policy pool，被 skills/tools 调度                                         |
| VLM 输入 | goal、图像、history、correction、constraints        | observation、role identity、task memory、working memory、tool/status feedback |
| VLM 输出 | `next_subtask JSON` 或 canonical skill command | skill/tool/policy 调度决策、retry/replan/human escalation                      |
| VLA 输入 | observation、proprioception、canonical subtask  | RoboClaw 生成的 instruction $l_t$、observation $o_t$、joint state $q_t$        |
| VLA 输出 | action chunk 或 action tokens                  | 单个 policy rollout 的 action chunk，由 MCP tool 启动/监控                         |
| 执行边界   | 子任务执行后再回到 VLM                                 | 每个子任务都通过 monitored execution、status polling 和 cleanup boundary            |

VLM+VLA 分层方案可以理解为一个模型训练与推理接口；RoboClaw 则把这个接口包进了 `Skills -> Tools -> Policies` 的层级中。RoboClaw 论文明确把 Policies 定义为产生低层动作的 VLA models，把 Tools 定义为 Start Policy、Terminate Policy、Env Summary 等 MCP 接口，把 Skills 定义为 orchestration procedures。来源：[RoboClaw](../summaries/roboclaw.md)。

## 3. 数据标注与采集对比

| 数据类型 | VLM+VLA 分层方案 | RoboClaw |
| --- | --- | --- |
| Episode goal / constraints | 训练 VLM 解析用户意图 | 写入 task-level memory，驱动 agent 计划与执行 |
| Subtask span / skill label | 同时生成 VLM 的 `next_subtask` 样本和 VLA 的 action 样本 | 作为 skill/policy invocation 的 prompt 和 success check |
| Correction layer | 主要训练 VLM；带动作轨迹的 motor correction 才训练 VLA | 变成 retry、replan、human intervention 和 recovery policy expansion 的触发信号 |
| Action trajectory | 训练 VLA behavior cloning / flow matching | 存入 dataset `D`，支持 forward policy 与 reset policy 迭代训练 |
| Run metadata | 可选诊断信息 | 核心数据：round logs、status logs、policy host/port、prompt、timeout、success/failure |
| Reset data | 通常不是主 schema | EAP 的核心：forward/reverse trajectory pairs |

VLM+VLA 方案的数据重点是把同一段 demonstration 切成 `episode -> subtask -> action_chunk -> outcome`。RoboClaw 的额外增量是 EAP：每个 forward rollout 后接 reverse/reset rollout，形成 $\tau_k = (\tau_k^{\rightarrow}, \tau_k^{\leftarrow})$，让环境回到可复用状态，并持续向 dataset `D` 加入 on-policy trajectories。来源：[RoboClaw](../summaries/roboclaw.md)。

## 4. Correction 与失败恢复对比

| 失败或纠正类型 | VLM+VLA 分层方案 | RoboClaw |
| --- | --- | --- |
| 语义选错对象 | correction 训练 VLM：`bad_subtask + correction -> corrected_subtask` | agent 更新 task/working memory，重选 skill 或 policy |
| 动作局部失败 | 若有 successful action trace，可微调 VLA recovery primitive | non-degrading failure 可 retry 同一 policy |
| 环境状态被破坏 | 需要额外 recovery data 或人工 reset | degrading failure 触发 recovery policy、replan 或 human intervention |
| 反复失败 | 通常记录为 hard negative / value signal | status monitoring 后停止、reset、切换 policy 或升级人工介入 |
| 从失败中学习 | 依赖人工整理 correction/outcome dataset | failure patterns 可逐步扩展 policy library 与 recovery policies |

简化理解：VLM+VLA 更像“把 correction 变成训练样本”；RoboClaw 更像“把 correction、status 和 failure pattern 变成运行时控制逻辑，并最终沉淀为新的 recovery policy”。这也是 RoboClaw 在长序任务上相对单个 `π0.5` baseline 的关键优势来源。来源：[RoboClaw](../summaries/roboclaw.md)，[VLA Data Annotation and Training](vla-data-annotation-and-training.md)。

## 5. 训练与微调路径对比

### 5.1 VLM+VLA 分层方案
推荐训练路径是：
1. 收集 demonstrations 并切分 subtask spans。
2. 训练 VLA：`observation + proprioception + subtask -> action_chunk`。
3. 训练 VLM：`goal + observation + history/correction -> next_subtask JSON`。
4. 用真实 corrections post-train VLM；只有带 successful motor trace 的 correction 才少量微调 VLA。

优点是训练目标清楚、数据 schema 简洁、调试边界明确。缺点是默认没有解决大规模自复位采集、policy pool 管理、部署时 progress monitoring 和 failure recovery。

### 5.2 RoboClaw
推荐训练路径更接近 lifecycle loop：
1. 为每个 manipulation behavior 准备 forward policy 和 inverse reset policy。
2. 用 EAP 自复位循环反复采集 forward/reverse trajectory pairs。
3. 将 human demonstrations、autonomously collected RoboClaw trajectories、failed rollout 后的 human interventions 共同纳入训练。
4. 用迭代 rollout 提升 subtask policies；论文报告每轮增加 `50` samples，1 到 5 轮后多个 forward policies 成功率持续提升。
5. 部署时继续把 execution trajectories 和 failure recovery 写回，扩充 policy pool 和 recovery behaviors。

优点是更贴近真实机器人运营，能把采集和部署分布对齐。缺点是工程负担重，且依赖稳定的 reset policy、MCP tool 层和状态监控。

## 6. 优劣与适用场景

| 选择 | 更适合的情况 | 主要优势 | 主要风险 |
| --- | --- | --- | --- |
| VLM+VLA 分层方案 | 先做可控原型、验证 annotation schema、训练一个任务族的 VLM planner + VLA policy | 简洁、模型接口清楚、数据标注成本可控 | 长序部署时容易缺少监控、reset、recovery 和持续采集闭环 |
| RoboClaw-style framework | 真实机器人长序部署、多 policy library、自主采集、需要减少人工 reset/intervention | 生命周期闭环强、EAP 降低人工 reset、运行时 recovery 更系统 | 工程复杂、对 skill/tool/policy infrastructure 依赖重、reset policy 不总是可行 |

如果当前目标是“我应该如何标注数据并训练 VLM/VLA”，应先采用 VLM+VLA 分层 schema。若目标升级为“机器人要在真实环境中持续采集数据、迭代 policy、完成多 policy 长序任务并从失败中恢复”，则应引入 RoboClaw-style lifecycle layer。

## 7. 实用折中方案
对实际项目，一个合理迁移路径是：

1. **Phase 1：最小 VLM+VLA**
   先建立 `goal -> subtask -> action_chunk` 数据契约，训练可执行的短技能 VLA 与能输出 JSON subtask 的 VLM。

2. **Phase 2：加入 monitored subtask execution**
   为每个 VLA rollout 增加 prompt、policy endpoint、timeout、status polling、success check 和 reset_after 等 metadata。这一步对应 RoboClaw 本地代码中的 `monitored-subtask-execution`。

3. **Phase 3：加入 EAP 数据采集**
   对可逆或可复位任务补 forward/reverse prompt pairs，记录 round logs 与 dataset episodes。这一步对应 RoboClaw 的 `eap-data-collection`。

4. **Phase 4：加入 recovery policy pool**
   将 degrading failures 后的人类恢复或自动恢复整理为 recovery policies，让 agent 在部署时可选择 retry、reset、replan 或 recovery policy。

这样可以避免一开始就承担 RoboClaw 的全部系统复杂度，又保留向 agentic lifecycle framework 演进的路径。

## 8. 潜在冲突或例外情况
- RoboClaw 论文使用 `π0.5` 作为底层 policy，因此它与 `π0.5` 类 VLM+VLA 并非竞争关系；RoboClaw 的贡献更多在系统闭环与 orchestration。
- 如果任务没有稳定 inverse reset behavior，EAP 的收益会明显下降，此时仍需人工 reset 或模拟/程序化 reset。
- 如果任务只有短时程单技能，RoboClaw 的 structured memory、skill layer 和 MCP tool orchestration 可能是过度工程。
- 如果 low-level VLA 还不可靠，RoboClaw 的监控与重试能缓解但不能根治 motor primitive 本身能力不足。

## 9. 相关页面
- 摘要页：[RoboClaw](../summaries/roboclaw.md)
- 综合页：[VLA Data Annotation and Training](vla-data-annotation-and-training.md)
- 相关摘要：[π0.5](../summaries/pi0-5.md)
- 相关摘要：[Hi Robot](../summaries/hi-robot.md)
- 概念页：[Hierarchical Language Supervision for VLA](../concepts/hierarchical-language-supervision-for-vla.md)
