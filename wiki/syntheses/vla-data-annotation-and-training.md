---
tags: [EmbodiedAI, Robotics, VLM, VLA, Data_Annotation, Training_Recipe]
last_updated: 2026-05-03
source: [Zotero, Local]
status: [Draft]
---

# VLA 数据标注与训练（VLA Data Annotation and Training）

## 1. 问题背景
这里关注的是类似 `π0.5` 展示的长序任务（long-horizon tasks）：机器人需要在真实家庭或半结构化环境中，根据开放式指令连续完成多个子目标，例如整理厨房、把衣物放进篮子、把餐具放入水槽。对这类任务，关键问题不是“是否需要 VLM 或 VLA”，而是如何把二者的职责拆开，并让数据标注直接服务这种拆分。

`Yell At Your Robot`、`Hi Robot` 和 `π0.5` 可以被看作 VLA systems 监督方式的一条演进线：
- `Yell At Your Robot` 说明 human language corrections 可以作为 post-deployment training data。
- `Hi Robot` 说明如果要做开放式指令跟随，仅有 low-level robot demonstrations 不够，还需要加入 high-level language layer，必要时可使用 synthetic interactions。
- `π0.5` 说明广泛泛化需要混合 low-level robot data、semantic subtasks、verbal supervision 和 non-robot multimodal data。

合起来看，它们提示 VLA training data 应按层标注，而不是压成单个扁平的 `(observation, instruction, action)` tuple。一个实用架构是：**VLM 负责长序语义决策与纠正吸收，VLA 负责短时程动作执行**。证据来源：
- [Yell At Your Robot](../summaries/yell-at-your-robot.md)
- [Hi Robot](../summaries/hi-robot.md)
- [π0.5](../summaries/pi0-5.md)

## 2. 比较维度

| 维度 | Yell At Your Robot | Hi Robot | π0.5 |
| --- | --- | --- | --- |
| 主要监督瓶颈 | 人类纠正语言（human correction language） | 开放式 prompt grounding | 开放世界泛化（open-world generalization） |
| 中间表示 | 检索得到的 language skill command | 原子级 language skill command | semantic subtask text |
| 高层数据来源 | 真实 human interventions | human skill labels + synthetic prompts | human verbal guidance + semantic labels + web tasks |
| 低层 controller | 冻结的 LCBC policy | flow-based VLA（`π0`） | flow-matching action expert |
| 训练重点 | 从 `D_corr` post-training | 使用 synthetic interaction data 的 hierarchical training | heterogeneous co-training + post-training specialization |
| 对标注的最佳启发 | 保留 correction spans 和 override metadata | 标注短技能并生成/收集 user-side language | 保留 subtask-level semantics 和 cross-modal supervision |

## 3. 推荐架构：VLM 做任务层，VLA 做动作层
对类似 `π0.5` 的长序任务，推荐把系统拆成两个显式接口。

### 3.1 VLM / 高层语义 policy
VLM 的职责是把开放式用户目标、当前视觉状态、执行历史和用户纠正，转换为**下一步可执行的规范化子任务**。它可以每个子任务完成后运行，也可以像 `Hi Robot` 一样以较低频率周期性运行，并在用户插话时立即重算。来源：[Hi Robot](../summaries/hi-robot.md)，[π0.5](../summaries/pi0-5.md)

**VLM 输入**
- 当前或短历史图像：例如 wrist camera、third-person camera、mobile base camera。
- 用户目标：例如 `"put all dirty dishes in the sink, but leave the clean glass on the table"`。
- 当前执行上下文：已完成子任务、当前子任务、失败记录、可见物体状态。
- 用户纠正或约束：例如 `"not that cup, the blue one"`、`"only pick up trash"`。
- 可选 memory：上一轮 VLM 输出、对象候选、环境地图或 scene graph。

**VLM 输出**
- `subtask`：规范化子任务文本，例如 `"pick up the dirty plate on the counter"`。
- `arguments`：对象、位置、容器、工具等结构化参数。
- `stop_condition`：何时认为子任务完成，例如 `"plate is inside sink"`。
- `priority_or_constraint`：约束或偏好，例如 `"avoid clean glass"`。
- `handoff_status`：继续执行、请求澄清、任务完成或失败。

一个实用的输出格式可以是 JSON，而不是只输出自由文本：

```json
{
  "mode": "execute_subtask",
  "subtask": "pick up the dirty plate on the counter",
  "object": "dirty plate",
  "target": "sink",
  "constraints": ["do not move the clean glass"],
  "stop_condition": "dirty plate is in the sink"
}
```

### 3.2 VLA / 低层 action policy
VLA 的职责是把当前 observation 加上 VLM 给出的短子任务，转换为短时程动作 chunk。它不应被迫直接解决完整长序任务；长序 credit assignment 和用户偏好应主要留给 VLM 或更高层 policy。`π0.5` 的可迁移启发正是先预测 semantic subtask，再以 subtask 为条件生成 low-level continuous actions。来源：[π0.5](../summaries/pi0-5.md)

**VLA 输入**
- 当前视觉观测与短历史：`I_t` 或多视角图像。
- proprioception：关节角、夹爪状态、末端执行器位姿、base pose。
- VLM 生成的 canonical subtask：例如 `"pick up the dirty plate on the counter"`。
- 可选辅助 grounding：object crop、mask、bbox、目标位姿或 affordance hints。

**VLA 输出**
- 未来 `H` 步动作 chunk：例如 end-effector delta pose、joint commands、gripper open/close、base velocity。
- 或 action tokens：如果使用类似 `π0.5` pre-training 中的 FAST action tokenization。
- 可选低层状态：子任务完成概率、失败概率、是否需要高层重规划。

VLA 训练样本更像下面这样：

```json
{
  "images": ["front_rgb_t", "wrist_rgb_t"],
  "proprio": "robot_state_t",
  "instruction": "pick up the dirty plate on the counter",
  "action_chunk": [
    "move_ee_delta(...)", 
    "close_gripper", 
    "lift_ee_delta(...)"
  ],
  "segment_end": false
}
```

## 4. 数据标注 schema：围绕 VLM/VLA 接口设计
三篇论文共同指向一个五层标注 schema。核心原则是：**episode 级标签主要训练 VLM，segment 级动作主要训练 VLA，correction/outcome 同时服务系统诊断和 post-training**。

### 4.1 任务层（Task Layer）
对每个 episode 标注：
- user goal；
- constraints 或 preferences；
- success rubric；
- task switch events；
- environment 或 embodiment metadata。

示例：
- "make a vegetarian sandwich without tomatoes"
- "clean up only the trash, not dishes"
- "put the dishes in the sink"

用途：主要训练 VLM 解析用户意图、维护任务状态和判断整体成功。原因是 `Hi Robot` 和 `π0.5` 都说明 task-level semantics 无法仅从 motor traces 中恢复。来源：[Hi Robot](../summaries/hi-robot.md)，[π0.5](../summaries/pi0-5.md)

### 4.2 子任务层（Subtask Layer）
对每个短时间段标注：
- canonical subtask 或 skill label；
- start/end span；
- object referent；
- hand 或 effector，如果相关；
- stop condition 或 completion criterion。

示例：
- "pick up one slice of lettuce"
- "open the drawer"
- "put the shirt in the laundry basket"

用途：一份标签可以产生两类样本：
- VLM 样本：`observation + user_goal + history -> next_subtask`。
- VLA 样本：`observation + next_subtask + proprioception -> action_chunk`。

原因：`Hi Robot` 依赖 1 到 3 秒的 skill segments，`π0.5` 在 inference time 依赖 semantic subtask prediction。来源：[Hi Robot](../summaries/hi-robot.md)，[π0.5](../summaries/pi0-5.md)

### 4.3 纠正层（Correction Layer）
correction layer 的数据不应只记录一句用户说了什么，而应记录一次“系统正在做什么、用户为什么纠正、纠正后应该怎么继续”的交互事件。对 interventions 标注：
- raw user utterance；
- pre-correction observation；
- 当前 user goal、VLM 输出的 subtask、VLA 正在执行的 action chunk；
- correction type：negation、spatial adjustment、preference、recovery、task redirect、clarification；
- 它是 override 还是 augment 当前 subtask；
- duration 或 resume condition；
- correction 修复的是 low-level motor failure 还是 high-level decision error。
- corrected target：修订后的 subtask、澄清后的 constraint，或一段 human override action。
- post-correction outcome：纠正后是否成功，是否仍需 recovery。

示例：
- "move a bit to the left"
- "that's not trash"
- "use the sponge to open the bag wider"

原因：这是 `Yell At Your Robot` 的核心信号，也是 `Hi Robot` 的主要能力目标之一。来源：[Yell At Your Robot](../summaries/yell-at-your-robot.md)，[Hi Robot](../summaries/hi-robot.md)

### 4.3.1 Correction layer 的数据来源
实用上可以从四条路径获得 correction data。

1. **部署或评估时的真实用户插话**：机器人执行过程中，用户直接说 `"not that one"`、`"move left"`、`"put it in the other drawer"`。这是最有价值的数据，因为它来自真实 failure distribution。`Yell At Your Robot` 将这类 verbal interventions 存入 `D_corr`，再用于 high-level post-training。来源：[Yell At Your Robot](../summaries/yell-at-your-robot.md)

2. **human-gated / teleoperation 接管**：当机器人明显要失败或不安全时，人类暂停、接管或示范 recovery。这里同时得到语言纠正和动作轨迹；只有这种带动作轨迹的 correction，才适合直接用于 VLA fine-tuning。来源：[Yell At Your Robot](../summaries/yell-at-your-robot.md)，[Interactive Imitation Learning](../concepts/interactive-imitation-learning.md)

3. **事后复盘标注（post-hoc relabeling）**：对失败 episode 回放视频，标注“哪里错了、应该给什么纠正、正确下一子任务是什么”。这比在线插话便宜，但分布可能不如真实用户自然。它主要适合扩展 VLM 的 `current_state + bad_subtask -> corrected_subtask` 数据。

4. **合成 interjections / prompts**：像 `Hi Robot` 一样，基于已切分的 skill segments 和视觉上下文合成用户 prompt、interjection 和机器人 response。它适合冷启动 VLM 的交互能力，但需要 grounding consistency 过滤；不应当当作真实 VLA 动作监督。来源：[Hi Robot](../summaries/hi-robot.md)

建议每条 correction event 至少保存成如下结构：

```json
{
  "episode_id": "kitchen_023",
  "t_start": 128.4,
  "t_end": 133.1,
  "goal": "Put all dirty dishes in the sink, but leave clean cups on the table.",
  "pre_observation": ["front_rgb_t", "wrist_rgb_t"],
  "current_subtask": "pick up the clean glass on the table",
  "raw_correction": "not that one, that's clean",
  "correction_type": "negation_and_preference",
  "target_layer": "VLM",
  "corrected_subtask": "pick up the dirty plate on the counter",
  "updated_constraints": ["do not move clean cups"],
  "human_override_actions": null,
  "outcome_after_correction": "success"
}
```

### 4.4 Correction data 如何用于 VLM 与 VLA

#### 4.4.1 用于 VLM：把 correction 变成重规划与偏好学习数据
大多数自然语言 correction 首先应该训练 VLM，而不是 VLA。训练样本的目标是让 VLM 学会：看到当前图像、原始 goal、历史和用户纠正后，输出修订后的下一子任务或请求澄清。

典型 VLM SFT 样本：

```json
{
  "input": {
    "goal": "Put all dirty dishes in the sink, but leave clean cups on the table.",
    "history": ["picked up dirty bowl", "placed dirty bowl in sink"],
    "current_subtask": "pick up the clean glass on the table",
    "observation": "counter with clean glass and dirty plate",
    "user_correction": "not that one, that's clean"
  },
  "target": {
    "mode": "execute_subtask",
    "subtask": "pick up the dirty plate on the counter",
    "constraints": ["do not move clean cups"],
    "reason_for_revision": "previous subtask violated user preference"
  }
}
```

VLM 可以从 correction layer 学到四类能力：
- **错误纠正**：`bad_subtask + correction -> corrected_subtask`。
- **偏好更新**：把 `"that's clean"` 转成后续持续生效的 constraint。
- **任务重定向**：把 `"do the table first"` 转成新的 subtask priority。
- **澄清策略**：当 correction 含糊时输出 `ask_clarification`，而不是强行执行。

如果同时保存了 bad subtask 和 corrected subtask，还可以构造成 preference data：`rejected = current_subtask`，`chosen = corrected_subtask`，用于 DPO、ranking loss 或其他 preference fine-tuning。但证据状态应标注为方法延伸；三篇核心论文中最直接支持的是 high-level supervised post-training，而不是必须使用某个 preference algorithm。来源：[Yell At Your Robot](../summaries/yell-at-your-robot.md)，[Hi Robot](../summaries/hi-robot.md)

#### 4.4.2 用于 VLA：只有带动作轨迹的 motor correction 才直接训练动作
VLA 不应该直接吃所有 correction。像 `"that's not trash"`、`"I said vegetarian"`、`"use the blue bowl"` 这类语义纠正应进入 VLM；如果直接拿它们训练 VLA，动作模型会收到没有可执行动作目标的噪声。

只有当 correction 满足以下条件时，才适合进入 VLA training：
- failure 是 motoric 或 grounding-local，例如 grasp 偏了、靠得不够近、放置位置有偏差；
- 有对齐的 human override action、teleoperation recovery trajectory，或 correction 后成功执行的 action chunk；
- correction 可以规范化为低层可执行 instruction，例如 `"move a bit left"`、`"open the gripper wider"`、`"insert the sponge under the bag edge"`。

典型 VLA fine-tuning 样本：

```json
{
  "images": ["front_rgb_t", "wrist_rgb_t"],
  "proprio": "robot_state_t",
  "instruction": "move a bit left and re-grasp the plate",
  "raw_correction": "move a bit to the left",
  "action_chunk": [
    "delta_ee(x=0.00, y=0.03, z=0.00)",
    "open_gripper",
    "delta_ee(x=0.02, y=0.00, z=-0.04)",
    "close_gripper"
  ],
  "outcome": "success"
}
```

VLA 使用 correction data 的推荐方式：
- 先保持 VLA 冻结，只用 corrections 训练 VLM；这是 `Yell At Your Robot` 最直接支持的做法。来源：[Yell At Your Robot](../summaries/yell-at-your-robot.md)
- 当累计到足够多带 human override actions 的 motor corrections 后，再对 VLA 做小比例 fine-tuning，重点补 recovery primitives 和常见失败姿态。
- 训练时把 correction examples 与原始 demonstration examples 混合，避免 VLA 过拟合到“总在失败后恢复”的分布。
- 对 outcome 为 failure 的 correction 不直接当正样本；可以用于 failure classifier、value/reward model 或 hard negative，但不应作为 imitation target。

#### 4.4.3 分层路由规则
标注时应给每条 correction 一个 `target_layer`：

| correction 类型 | 例子 | 主要训练对象 | 训练目标 |
| --- | --- | --- | --- |
| 语义否定 | `"not that one"` | VLM | 改选 object/subtask |
| 偏好或约束 | `"no tomatoes"`、`"leave clean cups"` | VLM | 更新 constraints / memory |
| 任务重定向 | `"do the sink first"` | VLM | 重排 subtask priority |
| 澄清需求 | `"the other drawer"` | VLM | ask clarification 或 resolve referent |
| 空间微调 | `"move a bit left"` | VLA，如果有动作轨迹；否则 VLM 转成低层 subtask | 学习 local recovery action |
| 操作技巧 | `"use the sponge to open the bag wider"` | VLM + VLA | VLM 选择工具策略；VLA 学习对应动作 primitive |

简化原则：**没有 action trace 的 correction 训练 VLM；有 successful action trace 且失败来自 motor 层的 correction 才训练 VLA；兼具语义和动作的 correction 要拆成两条样本**。

### 4.5 结果层（Outcome Layer）
对每个 segment 或 chunk 记录：
- executed action chunk；
- proprioception 和 images；
- success 或 failure；
- failure mode；
- recovery action，如果有。

原因：如果后续要做 online RL 或 DAgger-style post-training，仅有 correction language 不够；还需要知道 correction 之后发生了什么。这一点部分来自 [Yell At Your Robot](../summaries/yell-at-your-robot.md) 的推断，并由本知识库中的 broader online post-training literature 支撑。

### 4.6 语义感知层（Semantic Perception Layer）
如果目标接近 `π0.5` 的开放世界泛化，还应给同一批图像或外部数据补充非动作语义标签：
- caption；
- object detection / localization；
- object state：脏、干净、打开、关闭、空、满；
- visual question answering；
- affordance 或可操作性标签。

用途：主要训练 VLM 的场景理解，也可作为 VLA 的辅助 grounding。`π0.5` 的 heterogeneous co-training 表明，非机器人 multimodal data 可以在 semantic subtask 层改善泛化，但它不能替代真实 robot action data。来源：[π0.5](../summaries/pi0-5.md)

## 5. 具体长序任务样例

### 5.1 样例 A：整理厨房餐具
用户目标：

```text
Put all dirty dishes in the sink, but leave clean cups on the table.
```

VLM 在第一个决策点的输入：

```json
{
  "goal": "Put all dirty dishes in the sink, but leave clean cups on the table.",
  "observation": "front image shows counter, sink, dirty plate, clean glass",
  "history": [],
  "user_correction": null
}
```

VLM 输出：

```json
{
  "mode": "execute_subtask",
  "subtask": "pick up the dirty plate on the counter",
  "object": "dirty plate",
  "target": "sink",
  "constraints": ["do not move clean cups"],
  "stop_condition": "dirty plate is grasped"
}
```

VLA 输入：

```json
{
  "images": ["front_rgb_t", "wrist_rgb_t"],
  "proprio": "joint_positions_and_gripper_t",
  "instruction": "pick up the dirty plate on the counter"
}
```

VLA 输出：

```json
{
  "action_chunk": [
    "move end-effector toward plate",
    "align gripper with plate edge",
    "close gripper",
    "lift plate"
  ],
  "needs_replan": false
}
```

完成后，VLM 再输出 `"move the dirty plate to the sink"`，然后 `"release the dirty plate into the sink"`。如果用户说 `"not that one, that's clean"`，这条 correction 应作为 VLM 的高层训练样本：`observation + prior_subtask + correction -> revised_subtask`，而不是直接变成连续动作标签。这个划分与 `Yell At Your Robot` 和 `Hi Robot` 的 correction/high-level layer 一致。来源：[Yell At Your Robot](../summaries/yell-at-your-robot.md)，[Hi Robot](../summaries/hi-robot.md)

### 5.2 样例 B：卧室衣物收纳
用户目标：

```text
Put the clothes on the floor into the laundry basket.
```

可标注的子任务序列：
1. `"navigate to the visible clothes pile"`
2. `"pick up the white shirt from the floor"`
3. `"put the white shirt into the laundry basket"`
4. `"pick up the dark sock from the floor"`
5. `"put the dark sock into the laundry basket"`
6. `"verify no clothes remain on the floor"`

VLM 训练目标是预测上述下一步语义子任务；VLA 训练目标是在每个短 segment 内执行抓取、移动、放置等动作。`π0.5` 报告的 `laundry basket`、`dishes in sink` 等 household tasks 正适合这种标注方式。来源：[π0.5](../summaries/pi0-5.md)

## 6. 推荐训练配方
这三篇论文更支持分阶段 recipe，而不是从第一天开始端到端 joint training。

### 6.1 Stage A：收集并切分 demonstrations
先采集 teleoperation 或 human-guided demonstrations，并切成短 segment：
- 每个 episode 有整体 goal、约束和 success rubric。
- 每个 segment 有 canonical subtask、起止时间、对象、动作轨迹和 outcome。
- 如果采集者能边操作边口述，可像 `Yell At Your Robot` 一样把 narration 对齐到 skill segments，以降低事后标注成本。来源：[Yell At Your Robot](../summaries/yell-at-your-robot.md)

### 6.2 Stage B：训练低层 VLA
先在多样、短时程、language-conditioned skills 上训练 low-level VLA 或 LCBC policy。
- 使用短而规范的 skill labels。
- 让这些 labels 保持可执行、与 embodiment 相关。
- 优先覆盖物体交互和 recovery primitives，而不是过早扩展 free-form prompts。
- 训练目标是 behavior cloning、action-token prediction 或 flow matching action generation。

原因：三套系统都假设开放式智能首先依赖可靠的 low-level skill substrate。来源：[Yell At Your Robot](../summaries/yell-at-your-robot.md)，[Hi Robot](../summaries/hi-robot.md)，[π0.5](../summaries/pi0-5.md)

### 6.3 Stage C：训练高层 VLM
训练第二层，把 observation 加 user intent 映射到 canonical subtasks 或 skill commands。
- 小项目可先使用封闭或半封闭的 subtask vocabulary。
- 如果需要更丰富的交互，可以允许用户自由说话，但把 model target 规范化为 canonical subtask string。
- 输出建议使用结构化 JSON；自由文本可以作为 `subtask` 字段，而不是整个接口。
- 训练目标是 supervised fine-tuning：`image/context + goal/history/correction -> next_subtask JSON`。

原因：`Hi Robot` 和 `π0.5` 都受益于显式化 high-level reasoning。来源：[Hi Robot](../summaries/hi-robot.md)，[π0.5](../summaries/pi0-5.md)

### 6.4 Stage D：用合成或异构监督扩展高层数据
如果 human high-level labels 稀缺：
- 可像 `Hi Robot` 一样，用 visual context 加 labeled skill 合成 plausible prompts、corrections 和 robot replies；
- 或像 `π0.5` 一样，在 captioning、localization 和 question answering 等 semantic tasks 上 co-train。

建议：
- synthetic data 主要用于 high-level language layer，不用于 low-level action supervision。
- 对 synthetic outputs 进行严格 grounding consistency 过滤。
- 对真实机器人数据保留更高权重，避免合成 prompt 把模型推向无法执行的子任务。

原因：论文支持用 synthetic 和 heterogeneous augmentation 增强语义层，但不支持把它们当作真实 motor traces 的替代品。来源：[Hi Robot](../summaries/hi-robot.md)，[π0.5](../summaries/pi0-5.md)

### 6.5 Stage E：系统集成与闭环评估
集成时可采用如下运行循环：
1. VLM 读取 `goal + observation + history`，输出 `next_subtask JSON`。
2. VLA 在 `next_subtask` 条件下运行若干 action chunks。
3. completion detector、人工标注或 VLM 判断子任务是否完成。
4. 如果完成，回到 VLM 规划下一子任务；如果失败，记录 failure mode 并触发 recovery 或用户纠正。

评估不应只看单步动作成功率，还应看：
- subtask prediction accuracy；
- subtask completion rate；
- long-horizon task progress；
- user correction recovery rate；
- high-level semantic mistakes 与 low-level motor mistakes 的比例。

### 6.6 Stage F：用真实用户纠正进行 post-train
机器人部署后，记录 correction language，并在 `D ∪ D_corr` 上 fine-tune high-level policy。
- 初始阶段保持 low-level policy 冻结。
- 用 corrections 教会系统 recovery strategies、preference alignment 和 disambiguation。
- 只有当失败明确来自 motoric 而非 semantic 层时，才进一步考虑更新 low-level control。

原因：`Yell At Your Robot` 说明小规模 correction datasets 已能产生显著 high-level gains。来源：[Yell At Your Robot](../summaries/yell-at-your-robot.md)

### 6.7 Stage G：可选 online RL 或 DAgger-style scaling
如果具备基础设施，可以在此基础上加入 online post-training：
- HG-DAgger-style imitation，用于 supervised correction loops；
- offline-to-online RL，当存在 reward 且 long-horizon credit assignment 很重要时使用。

这一步不是三篇焦点论文的主要贡献，但如果目标是 continuously improving deployed VLA system，它是自然延伸。

## 7. 实用建议
如果目标是构建自己的 VLM+VLA dataset，最高杠杆的 annotation priorities 是：
1. 带精确 temporal spans 的 canonical subtask labels。
2. episode level 的 constraint 和 preference language。
3. 带 correction-type tags 的真实 human correction utterances。
4. 每次 correction 后的 outcome 和 failure metadata。
5. 用于区分 semantic error 与 motor error 的诊断标签。

如果 annotation budget 紧张，不要先把预算花在打磨 free-form prompt diversity 上。优先投入：
1. 让 subtask ontology 稳定；
2. 收集 recovery 和 correction data；
3. 区分 high-level semantic mistakes 与 low-level execution mistakes。
4. 确保每个高频子任务至少有足够多不同物体、位置和初始姿态的 VLA action examples。

## 8. 潜在冲突或例外情况
- `Hi Robot` 偏向 open-ended promptability，而 `Yell At Your Robot` 更依赖 retrieval-friendly language bank。实用折中是允许 free-form input，但把 targets canonicalized。
- `π0.5` 使用非常广的数据混合，小实验室可能不现实；可迁移的 lesson 是 supervision hierarchy，而不一定是精确规模。
- 如果 low-level policy 很弱，更多 high-level annotation 本身可能帮助有限。此时应先补充 recovery primitives 和 motor data，再扩展 semantics。
- 端到端单模型也可以同时输出 subtask 与 action，但数据契约仍建议显式保留这两个 target；否则调试时很难判断失败来自语义规划还是运动控制。

## 9. 相关页面
- [Hierarchical Language Supervision for VLA](../concepts/hierarchical-language-supervision-for-vla.md)
- [Yell At Your Robot](../summaries/yell-at-your-robot.md)
- [Hi Robot](../summaries/hi-robot.md)
- [π0.5](../summaries/pi0-5.md)
