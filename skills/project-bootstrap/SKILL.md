---
name: project-bootstrap
description: Bootstrap a new or nearly-empty software project into a right-sized engineering harness. Use when starting a new project, creating its AGENTS.md, choosing project profiles, defining verification gates, or turning a rough project idea into durable repository conventions. Do not use to redesign a mature existing repository; use project-adopt instead.
---

# Project Bootstrap

目标是建立最小但可演化的项目 Harness，不开始无关应用实现。

## 1. 建立 Project Intake

优先从用户描述、现有文件、Git 配置、依赖文件和目录结构自动获取信息。

对关键判断标记：

- `confirmed`
- `inferred`
- `unknown`
- `N/A`

只追问会明显改变架构、安全、外部行为、长期维护成本、不可逆选择或继续执行所必需的 `unknown`。

详细检查域见 `references/intake-checklist.md`。

## 2. 选择 Profile

只在需要时读取 `references/profiles/`。Profile 是默认决策，不是强制模板，现实项目证据优先。

可组合多个 Profile，例如 `go-library + agent-core`。

## 3. 应用工程默认值

需要生成项目长期规则时，读取 `references/engineering-defaults.md` 和 `assets/AGENTS.repo.template.md`，只保留当前项目真实适用的部分。

不要把个人偏好复制成多个 source of truth。

## 4. 建立 Source of Truth

先识别每类信息未来唯一的权威位置：

- 项目规则：`AGENTS.md`
- 项目事实：README / docs / code / config
- 验证：Makefile / scripts / CI
- 当前状态：Issue / PR / Roadmap

不要创建阶段性快照或互相覆盖的规则文件。

## 5. 生成最小 Harness

按需要创建，而不是全部创建：

- `AGENTS.md`
- README / 必要长期 docs
- 项目级 Agent Skills
- 当前客户端支持的低歧义安全 adapter（如果确实需要）
- Makefile / scripts
- GitHub Issue / PR / CI

模板资源在 `assets/` 下，只在匹配项目需求时使用。

如果只是实验项目，允许只创建极少文件。

## 6. 机械约束优先

能用测试、脚本、权限、平台安全机制或 CI 可靠表达的约束，不只写成自然语言要求。

平台特有能力必须被识别为平台特有能力，不把 Codex Hook、Claude Hook 等描述成跨平台标准。

## 7. 验证

完成后：

1. 检查新文件内部引用是否存在。
2. 检查项目 Skill frontmatter 与触发条件。
3. 验证脚本至少能通过语法/帮助路径运行。
4. 运行项目已有门禁或等价检查。
5. 报告 confirmed / inferred / unknown / 未验证。

Bootstrap 完成后不要自动开始无关业务实现。
