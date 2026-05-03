---
tags: [EmbodiedAI, KnowledgeBase, Log]
last_updated: 2026-05-03
source: [Zotero, Local, Web]
status: [Draft]
---

# Operation Log

## [2026-05-03] ingest | kai0 resource-aware robust manipulation
- Sources: Zotero, Local, Web
- Added: `wiki/summaries/kai0-resource-aware-robust-manipulation.md`, `wiki/concepts/advantage-modeling-for-vla.md`, `wiki/syntheses/kai0-stage-advantage-vs-recap-value-function.md`
- Updated: `wiki/index.md`, `wiki/concepts/offline-to-online-rl-for-vla.md`, `wiki/concepts/online-post-training-for-vla.md`, `wiki/summaries/pi-star-0-6-recap.md`
- Notes: 使用 Zotero item `MNPQV5ZH`、arXiv v3、项目页和本地 `/Users/ruanyifan/code/kai0` commit `9d93078c757840f50e75248c5c5a94ab7b41e13a` 总结 KAI0；重点比较 KAI0 Stage Advantage 与 RECAP 在 value/advantage function 建模、policy conditioning、优劣边界和数据规模口径上的差异。PDF 本地归档待补。

## [2026-05-03] ingest | sop and learning while deploying
- Sources: Zotero, Local
- Added: `raw/learning_while_deploying/paper.pdf`, `raw/sop_a_scalable_online_post_training_system_for_vision_language_action_models/paper.pdf`
- Added: `wiki/summaries/learning-while-deploying.md`, `wiki/summaries/sop-scalable-online-post-training-system.md`
- Added: `wiki/concepts/online-post-training-for-vla.md`, `wiki/syntheses/sop-vs-learning-while-deploying.md`
- Updated: `wiki/index.md`
- Notes: Retrieved two RL-related VLA post-training papers from Zotero and summarized their algorithmic and system-level differences.

## [2026-05-03] ingest | hi robot, yell at your robot, pi0.5
- Sources: Zotero, Local
- Added: `raw/hi_robot_open_ended_instruction_following_with_hierarchical_vision_language_action_models/paper.pdf`, `raw/yell_at_your_robot_improving_on_the_fly_from_language_corrections/paper.pdf`, `raw/pi0_5_a_vision_language_action_model_with_open_world_generalization/paper.pdf`
- Added: `wiki/summaries/hi-robot.md`, `wiki/summaries/yell-at-your-robot.md`, `wiki/summaries/pi0-5.md`
- Added: `wiki/concepts/hierarchical-language-supervision-for-vla.md`, `wiki/syntheses/vla-data-annotation-and-training.md`
- Updated: `wiki/index.md`
- Notes: Summarized three VLA papers on language interaction and open-world generalization, then distilled a reusable annotation and training recipe for hierarchical VLA systems.

## [2026-05-03] revision | wiki 中文化与术语规范
- Sources: Local
- Updated: `AGENTS.md`, `wiki/index.md`, `wiki/summaries/`, `wiki/concepts/`, `wiki/syntheses/`
- Notes: 将核心 wiki 页面迁移为中文主文，保留论文标题、模型名、算法名、缩写、Zotero key、DOI 和 Markdown 链接目标；在 `AGENTS.md` 中新增“关键术语首现双语、后文保留英文专名/缩写”的长期写作习惯。

## [2026-05-03] ingest | recap and hg-dagger iteration cost
- Sources: Zotero, Local
- Added: `raw/pi_star_0_6_a_vla_that_learns_from_experience/paper.pdf`, `raw/hg_dagger_interactive_imitation_learning_with_human_experts/paper.pdf`
- Added: `wiki/summaries/pi-star-0-6-recap.md`, `wiki/summaries/hg-dagger.md`
- Added: `wiki/concepts/recap.md`, `wiki/concepts/hg-dagger.md`, `wiki/syntheses/sop-recap-hg-dagger-iteration-cost.md`
- Updated: `wiki/summaries/sop-scalable-online-post-training-system.md`, `wiki/concepts/online-post-training-for-vla.md`, `wiki/index.md`
- Notes: 挖掘 SOP 所用 HG-DAgger 与 RECAP 的原始算法来源，整理 iteration 定义、SOP 在线化后的更新语义、3 小时实验预算、checkpoint cadence，以及 RECAP 每轮采集时长的可追溯上界估计。

## [2026-05-03] verification | pdftotext recap and hg-dagger
- Sources: Local
- Updated: `wiki/summaries/pi-star-0-6-recap.md`, `wiki/syntheses/sop-recap-hg-dagger-iteration-cost.md`
- Notes: 使用 `pdftotext -layout` 复核 SOP、RECAP、HG-DAgger 三篇 PDF，确认原有结论未被推翻；补充 RECAP 中“任务总体 5-15 分钟”与 quantitative evaluation timeout 的口径差异。

## [2026-05-03] revision | merge sop iteration cost
- Sources: Local
- Updated: `wiki/summaries/sop-scalable-online-post-training-system.md`, `wiki/index.md`, `wiki/concepts/`, `wiki/summaries/`
- Removed: `wiki/syntheses/sop-recap-hg-dagger-iteration-cost.md`
- Notes: 将独立的 SOP/RECAP/HG-DAgger 迭代成本综合页合并回 SOP 摘要页，并清理相关页面中的旧链接。

## [2026-05-03] audit | concept-page type correction
- Sources: Local, Web
- Added: `wiki/concepts/offline-to-online-rl-for-vla.md`, `wiki/concepts/interactive-imitation-learning.md`
- Removed: `wiki/concepts/recap.md`, `wiki/concepts/hg-dagger.md`
- Updated: `wiki/index.md`, `wiki/concepts/online-post-training-for-vla.md`, `wiki/summaries/pi-star-0-6-recap.md`, `wiki/summaries/hg-dagger.md`, `wiki/summaries/sop-scalable-online-post-training-system.md`, `wiki/summaries/learning-while-deploying.md`
- Notes: 将 RECAP 和 HG-DAgger 从概念层下沉为论文/方法名，改用 offline-to-online RL 与 interactive imitation learning 承接抽象概念；补充 LWD 项目页日期和 HG-DAgger DOI。

## [2026-05-03] revision | rlinf local reference implementations
- Sources: Local
- Updated: `AGENTS.md`, `wiki/index.md`, `wiki/summaries/hg-dagger.md`, `wiki/summaries/pi-star-0-6-recap.md`, `wiki/summaries/sop-scalable-online-post-training-system.md`, `wiki/concepts/interactive-imitation-learning.md`, `wiki/concepts/offline-to-online-rl-for-vla.md`
- Notes: 将本地 `/Users/ruanyifan/code/RLinf` commit `6fb1d3fdf694b59550f500c81c057343e71871b5` 作为 HG-DAgger 和 RECAP 的参考实现关联到现有知识页；明确该仓库不是论文 original implementation，并在 `AGENTS.md` 中新增 `/Users/ruanyifan/code/` 已有代码仓优先复用、不得重复下载的长期规则。

## [2026-05-03] query writeback | vlm-vla long-horizon annotation
- Sources: Local
- Updated: `wiki/syntheses/vla-data-annotation-and-training.md`, `wiki/index.md`
- Notes: 根据用户对 `π0.5` 类长序任务的关注，补充 VLM 与 VLA 的职责边界、输入输出样例、长序任务标注 schema、VLM/VLA 分阶段训练与 deployment correction post-training 建议。

## [2026-05-03] query writeback | correction layer for vlm-vla training
- Sources: Local
- Updated: `wiki/syntheses/vla-data-annotation-and-training.md`, `wiki/log.md`
- Notes: 补充 correction layer 的四类数据来源、事件级标注 schema、VLM supervised/replanning/preference 使用方式、VLA motor correction 使用前提，以及按 correction 类型路由到 VLM/VLA 的规则。
