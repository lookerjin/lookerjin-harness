---
name: harness-evolve
description: Review repeated friction from real development and decide whether it should become a durable AGENTS rule, Skill, Hook, script, profile default, or remain project-local. Use after several development cycles, repeated corrections, recurring CI/debug failures, or when the user wants to improve their personal harness from observed evidence.
---

# Harness Evolve

目标是从真实反馈中提炼 Harness，而不是为完整性增加配置。

## 输入证据

按需查看：

- 最近反复出现的用户纠正。
- Git / PR / Issue / CI 失败模式。
- 项目 `AGENTS.md`、`.agents/skills`、hooks、scripts。
- 已有个人 Harness，避免重复。
- 多项目共同模式。

## 分类

每个候选改进先路由：

- 始终成立的长期规则 → AGENTS
- 特定任务的可复用流程 → Skill
- 机械安全/生命周期约束 → Hook / permission / policy
- 确定性重复执行 → Script / Makefile / CI
- 项目事实 → Docs
- 当前状态 → Issue / PR / Roadmap
- 外部系统/当前外部知识 → MCP / Plugin

## Promotion Gate

个人 Harness 候选至少满足：

- 跨两个项目出现；或
- 同一项目被纠正 2～3 次；或
- 属于高风险事故防重复；或
- 能显著减少重复操作；或
- 已能写清 trigger / input / output / verification。

## 反向检查

同时寻找应该删除的东西：

- 已被模型原生能力稳定覆盖的通用提示。
- 重复 source of truth。
- 误触发频繁的 Skill。
- 误拦截明显的 Hook。
- 没人使用的模板或脚本。

## 输出

先给候选变更和证据，再修改 Harness。不要把一次性经验直接提升到个人层。
