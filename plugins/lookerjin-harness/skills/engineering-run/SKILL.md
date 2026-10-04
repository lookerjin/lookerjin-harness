---
name: engineering-run
description: Route a software engineering task from intent to verifiable outcome using a right-sized playbook and existing skills. Use for implementing features, investigating systems, fixing defects, preserving behavior during refactors, exploring prototypes, or carrying a multi-step task to completion. For a narrow task already owned by a specific skill, use that skill directly. Do not use for casual discussion or as authorization to commit, push, publish, or create PRs.
---

# Engineering Run

把任务推进到可检查的结果。只加载匹配的 Playbook 和当前阶段需要的能力。

本入口属于软件工程 Domain Harness，负责领域任务路由、验收和能力组合。具体语言知识与专业审查优先复用当前客户端的专家插件/工具；不在这里维护对应规则库、安装流程或专用执行引擎。专业结果通过 Change Review 核对覆盖、行为证据并收敛，不重复运行已经覆盖同一目标的流程。

## 路由

先明确用户要的是解释、行为变化、行为保持、决策实验还是持续执行。不要把“看看为什么”变成自动修复。

| 用户目标 | 读取 | 完成条件 |
|---|---|---|
| 理解、诊断、比较，未要求修改 | [investigate](references/playbooks/investigate.md) | 有证据的解释与边界 |
| 新增或改变行为 | [feature](references/playbooks/feature.md) | 验收行为得到验证 |
| 修复已报告缺陷 | [bug-fix](references/playbooks/bug-fix.md) | 原触发路径不再失败 |
| 保持行为，改变结构 | [refactor](references/playbooks/refactor.md) | 原行为契约保持 |
| 用低成本实验做决策 | [prototype](references/playbooks/prototype.md) | 观察结果足以选取或放弃方向 |
| 多个相依步骤或批量任务 | [long-run](references/playbooks/long-run.md) | 可检查的整体完成条件成立 |

混合任务选一个主 Playbook；`long-run` 只协调 Units，各 Unit 使用更具体的流程。初始化、接入、依赖评估、评审、演化和评估直接交给现有对应 Skill，不绕一遍本入口。发现目标变了，说明变化并重新路由。

## 推进

1. 读取适用项目规则和直接相关事实，记录用户已有修改与授权范围。
2. 写出一句目标、修改范围、验收行为和验证入口。复杂任务使用短计划；已知原因的小改动直接执行，省略不产生信息的步骤。
3. 读取 [execution-contract](references/execution-contract.md)，选定 Playbook，调用或读取当前阶段需要的 Skill。工具不可用时顺序执行并说明限制；不假装能力已运行。
4. 每次推进依赖运行或源码证据。门槛不满足时回到能获取缺失信息的阶段；有明确外部阻塞时报告最小解除动作。
5. 做完修改后执行项目验证和 [change-review](../change-review/SKILL.md)，修复发现的问题，再运行受影响检查。
6. 汇报结果、关键证据、未验证项和剩余阻塞。没有外部授权时，交付可审查的本地结果。

已有事实足够时跳过重复调查；不要为形式完整先读取全部 Playbook。多 Agent、多模型和并行是当前客户端提供的可选执行方式，不是完成任务的前提，也不通过这里授予启动权限。
