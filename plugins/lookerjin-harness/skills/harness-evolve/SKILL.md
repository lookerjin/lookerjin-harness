---
name: harness-evolve
description: Review repeated friction from real development and decide whether it should become a portable Agent Skill, project AGENTS rule, deterministic script, platform adapter, or remain project-local. Use after several development cycles, repeated corrections, recurring CI/debug failures, or when improving this personal Agent Plugin from observed evidence. Do not use without repeated evidence.
---

# Harness Evolve

目标是从真实反馈中提炼 Harness，而不是为完整性增加配置。没有重复证据时直接停止，不要为了演化而演化。

晋升门槛以 [promotion-policy](references/promotion-policy.md) 为唯一来源；按需读取 [surface-routing](references/surface-routing.md) 和 [integrations](references/integrations.md)。

## 输入证据

按需查看用户重复纠正、Git/PR/Issue/CI 失败模式、项目规则与 Skills、现有插件能力，以及多项目共同模式。

只读取当前任务明确相关且可访问的 transcript 或已有原始产物，不全盘扫描其他会话或客户端用户目录；没有 transcript 时用有来源的会话摘要，不虚构调用轨迹。

为候选记录问题、独立发生的项目/周期、证据位置、影响、已尝试处理和反例。同一次失败的日志、CI 与聊天摘要是一个事件，不算三次重复；区分 Skill 缺失、误触发、未遵循、工具不可用与项目特有约束，再决定修改位置。

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

按 Promotion Policy 核对重复证据和复用边界。触发器写得清楚、文档更漂亮不等于已证明有效；行为变化使用 [harness-eval](../harness-eval/SKILL.md) 比较原始结果，无法运行时明确未验证，不自动晋升。

同时主动删除重复 source of truth、低价值通用提示、误触发 Skill、误拦截 adapter 和无人使用资源。
