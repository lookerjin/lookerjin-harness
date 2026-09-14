---
name: project-bootstrap
description: Bootstrap a new or nearly-empty software project into a right-sized engineering harness. Use when starting a new project, creating its AGENTS.md, choosing project profiles, defining verification gates, or turning a rough project idea into durable repository conventions. Do not use to redesign a mature existing repository; use project-adopt instead.
---

# Project Bootstrap

目标是建立最小但可演化的项目 Harness，不开始无关应用实现。

## 1. 先建立 Project Intake

优先从用户描述、现有文件、Git 配置、依赖文件和目录结构自动获取信息。

对每个关键判断标记：

- `confirmed`
- `inferred`
- `unknown`
- `N/A`

只追问会明显改变架构、安全、外部行为、长期维护成本、不可逆选择或继续执行所必需的 `unknown`。

详细检查域见 `references/intake-checklist.md`。

## 2. 选择 Profile

从个人 Harness 的 `profiles/` 中选择 0 个或多个最贴近项目的 Profile。

Profile 是默认决策，不是强制模板。现实项目证据优先。

## 3. 建立 Source of Truth

先识别每类信息未来唯一的权威位置：

- 项目规则：`AGENTS.md`
- 项目事实：README / docs / code / config
- 验证：Makefile / scripts / CI
- 当前状态：Issue / PR / Roadmap

不要创建重复页面、阶段性快照或一组互相覆盖的规则文件。

## 4. 生成最小 Harness

按需要选择，而不是全部创建：

- `AGENTS.md`
- README
- 必要的长期 docs
- `.agents/skills` 项目 Skill
- `.codex/hooks.json` 与 hook handler
- Makefile / scripts
- GitHub Issue / PR / CI 模板

如果项目很小或只是实验，允许只创建 README 或极少文件。

## 5. 机械约束优先

能用测试、脚本、Hook 或 CI 可靠表达的约束，不只写成自然语言要求。

Hook 只处理低歧义、高价值机械检查；不要把复杂架构判断放进 Hook。

## 6. 验证

完成后：

1. 检查新文件内部引用是否存在。
2. 检查 Skill frontmatter 与触发条件。
3. 验证脚本至少能通过语法/帮助路径运行。
4. 如果 Harness Doctor 可用，运行 Doctor。
5. 报告 confirmed / inferred / unknown / 未验证。

## 7. 停止条件

Bootstrap 完成后不要自动开始实现业务功能，除非用户的当前请求明确同时要求实现。
