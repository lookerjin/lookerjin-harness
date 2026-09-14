# lookerjin-harness

一套面向 Codex Desktop 的个人开发 Harness。

目标不是把所有开发过程塞进一个超级提示词，而是把长期规则、可复用流程、确定性检查、外部能力和项目事实分层，让它们各自只有一个清晰职责。

## 设计原则

- **AGENTS.md**：长期稳定、在当前作用域内始终成立的规则与索引。
- **Skill**：只在特定任务触发的可复用流程、专业知识和编排方法。
- **Hook**：适合机械拦截或生命周期检查的确定性约束。
- **Script / Makefile / CI**：可重复、可验证的确定性执行。
- **Docs**：项目事实、架构、契约、需求与长期设计。
- **GitHub**：Issue、PR、CI 与协作状态的权威来源。
- **MCP / Plugin**：连接外部系统或获取当前外部知识，不复制项目内部事实。
- **Codex Browser**：优先承担交互式 Web 验证；只有需要可重复 E2E/CI 时才引入 Playwright。

Harness 应该通过真实项目逐步演化。没有反复出现的痛点，不提前固化。

## 目录

```text
lookerjin-harness/
├── README.md
├── global/
│   ├── AGENTS.md
│   ├── config.toml
│   ├── hooks/
│   └── rules/
├── skills/
│   ├── project-bootstrap/
│   ├── project-adopt/
│   ├── root-cause-debug/
│   ├── dependency-evaluation/
│   ├── change-review/
│   └── harness-evolve/
├── profiles/
│   ├── go-library/
│   ├── go-service/
│   ├── agent-core/
│   ├── web-app/
│   └── experiment/
├── assets/
│   ├── agents/
│   ├── github/
│   ├── makefile/
│   └── scripts/
└── checks/
    └── harness-doctor/
```

## V1 使用方式

### 1. 安装个人层

先预览：

```bash
python assets/scripts/install-user.py
```

确认后执行：

```bash
python assets/scripts/install-user.py --apply
```

脚本默认：
- 不覆盖已有 `~/.codex/AGENTS.md`、`config.toml` 或 `hooks.json`。
- 将本仓库 `skills/` 安装到 `$HOME/.agents/skills`。
- Unix 优先使用符号链接，Windows 默认复制；可通过参数调整。
- 如果目标文件已存在，会报告冲突并停止该项安装。

个人 `config.toml` 只是建议基线，不会自动覆盖现有 Codex 配置。

### 2. 新项目

在 Codex Desktop 中打开目标项目后：

```text
$project-bootstrap
```

Bootstrap 应先扫描真实项目，再建立 Project Intake。未知信息使用四态标记：

- `confirmed`：由用户、代码、配置或权威项目资料直接确认。
- `inferred`：基于证据推断，但尚未得到直接确认。
- `unknown`：会影响结果且当前无法可靠确定。
- `N/A`：对当前项目不适用。

只追问会明显改变架构、安全、外部行为、长期维护成本或不可逆选择的 `unknown`。

### 3. 接入已有项目

```text
$project-adopt
```

原则是 scan → compare → gap analysis → minimal adoption，不覆盖已有规则和工作流。

### 4. 日常开发

常用个人 Skill：

- `$root-cause-debug`：先证据、最小实验，再修复。
- `$dependency-evaluation`：评估外部依赖与自研边界。
- `$change-review`：实现完成后的 diff、证据和未验证项审查。
- `$harness-evolve`：把重复出现的工作方式提炼回 Harness。

### 5. Harness 健康检查

```bash
python checks/harness-doctor/doctor.py --root .
```

Doctor 只做确定性或低歧义检查，不替代模型做架构判断。

## Profile 的角色

Profile 不是 starter repo，也不是大而全模板。它只提供某一类项目的默认决策和“通常应该考虑什么”。

当前 V1：

- `go-library`：可复用 Go 库。
- `go-service`：长期运行的 Go 后端服务。
- `agent-core`：Agent Runtime / Core / Harness。
- `web-app`：需要真实浏览器验证的 Web 应用。
- `experiment`：低成本、短生命周期验证。

Profile 可以组合。比如 Agent Core 可以在 `go-library` 基础上追加状态、恢复、安全、Provider 隔离与评测要求。

## 外部能力建议

V1 默认保持很薄：

- **GitHub**：Issue / PR / CI / 远端状态。
- **Context7 MCP**：只用于外部库、SDK、API 和版本行为；项目内部事实优先读仓库。
- **Codex Browser / CDP**：交互式 Web 验证。
- **Playwright**：只有当验证需要进入可重复 E2E 或 CI 时，作为项目依赖引入，而不是为了给 Codex“一个浏览器”。
- **Serena / Beads / RTK / Caveman / 大型 Skill Pack**：先不默认安装，只有真实 profiling 证明存在对应痛点时再引入。

## 信息应该放在哪里

详见 `global/rules/surface-routing.md`。最短判断：

```text
始终成立的规则      -> AGENTS.md
某类事情怎么做      -> Skill
能机械禁止/拦截      -> Hook / permission / policy
能确定性执行         -> Script / Makefile / CI
项目现在是什么       -> Docs / code / config
项目现在做到哪       -> GitHub Issue / PR / Roadmap
外部当前知识/系统     -> MCP / Plugin / Web
```

## 从 Pizza 得到的经验

Pizza 是本 Harness 的第一个 reference project，但个人 Harness 不复制 Pizza 的项目事实。可迁移的是这些模式：

- 权威资料按职责拆分，避免多个 source of truth。
- Makefile / scripts 承担确定性门禁，Skill 只做编排和判断。
- 恢复、安全、工具副作用等高风险语义使用项目级 Skill 审查。
- 未运行、部分覆盖、未知状态如实记录。
- 新增依赖先验证成熟实现与替换边界。
- 开发结束时检查 diff、证据、未追踪文件和未验证项。

## 演化门槛

一项规则或流程进入个人 Harness，至少满足其一：

1. 在两个以上项目重复出现。
2. 同一项目已经被人工纠正 2～3 次。
3. 属于严重事故或高风险行为的防重复机制。
4. 能显著减少认知负担或重复操作。
5. 可以写出明确的 trigger、input、output 和 verification。

只发生一次的问题，优先留在项目层。

## 设计依据

官方资料：

- Codex Customization / AGENTS / Skills / MCP / Hooks：<https://learn.chatgpt.com/docs/customization/overview>
- Build Skills：<https://learn.chatgpt.com/docs/build-skills>
- Hooks：<https://learn.chatgpt.com/docs/hooks>
- Advanced Config：<https://learn.chatgpt.com/docs/config-file/config-advanced>
- OpenAI Cookbook：Iterating development workflows with Codex：<https://github.com/openai/openai-cookbook/blob/main/examples/codex/iterating-development-workflows-with-codex.md>
- OpenAI Plugins examples：<https://github.com/openai/plugins>

社区经验主要作为方向性证据使用，不作为规范来源：近年的 Codex 社区反馈普遍倾向于减少大而全 Skill Pack，把能力收敛到项目特有流程、验证、调试、依赖/文档获取和确定性门禁。

## 当前状态

这是 V1。先用真实项目验证，再演化，不追求一次设计完整。
