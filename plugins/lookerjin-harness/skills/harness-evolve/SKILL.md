---
name: harness-evolve
description: Review repeated friction from real development and decide whether it should become a portable Agent Skill, project AGENTS rule, deterministic script, platform adapter, or remain project-local. Use after several development cycles, repeated corrections, recurring CI/debug failures, or when improving this personal Agent Plugin from observed evidence. Do not use without repeated evidence.
---

# Harness Evolve

目标是从真实反馈中提炼 Harness，而不是为完整性增加配置。没有重复证据时直接停止，不要为了演化而演化。

需要时读取 `references/promotion-policy.md`、`references/surface-routing.md` 和 `references/integrations.md`。

## 输入证据

按需查看用户重复纠正、Git/PR/Issue/CI 失败模式、项目规则与 Skills、现有插件能力，以及多项目共同模式。

## 路由

- 跨平台、特定任务可复用流程 → Agent Skill
- 项目长期规则 → 项目 `AGENTS.md`
- 可确定性执行 → Script / Makefile / CI
- 外部系统或当前外部知识 → MCP
- 客户端特有 Hook / Command / Agent / 权限配置 → 反向域名 client extension / adapter
- 项目事实 → Docs / code / config
- 当前状态 → Issue / PR / Roadmap
- 一次性要求 → 当前线程

不要创建 Agent Plugins 1.0 没有定义的自定义 portable component。

## Promotion Gate

候选至少满足一个条件：跨项目重复、同项目多次纠正、高风险防重复、显著减少重复劳动，或已经能明确 trigger/input/output/verification。

同时主动删除重复 source of truth、低价值通用提示、误触发 Skill、误拦截 adapter 和无人使用资源。
