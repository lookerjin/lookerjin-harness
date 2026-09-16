# lookerjin-harness

一个面向 AI Coding Agent 的 Developer Domain Harness，按 Agent Plugins 1.0 组织。

它负责跨项目可复用的软件工程工作流、验证方式和演化方法；具体语言、框架或工具的专业知识优先交给独立 Expert Plugin，而不是继续膨胀本 Harness。

本插件位于 Marketplace 仓库的：

```text
plugins/developer/lookerjin-harness/
```

## 定位

`lookerjin-harness` 是 Developer 领域的元插件 / Domain Harness。这里的“元插件”是架构角色，不是新的 Agent Plugins 协议类型。

它主要回答：

- 项目应该怎样初始化或接入；
- 问题应该怎样定位根因；
- 新依赖应该怎样评估；
- 变更应该怎样审查和验证；
- 哪些重复摩擦值得沉淀进 Harness；
- 哪些问题应该交给独立专家插件或外部工具。

它不试图成为 Go、Python、TypeScript、数据库、安全或前端知识大全。

## 架构

```text
lookerjin-harness/
├── plugin.json
├── mcp.json
├── AGENTS.md
├── docs/
└── skills/
    ├── project-bootstrap/
    ├── project-adopt/
    ├── root-cause-debug/
    ├── dependency-evaluation/
    ├── change-review/
    ├── harness-evolve/
    └── harness-doctor/
```

Agent Plugins 1.0 的 portable component 只有 Skills 和 MCP Servers。本插件不自定义第三套插件协议。

`docs/` 只是插件级文档和实地验证记录，不是 Agent Plugins component，也不参与插件发现。

根目录 `AGENTS.md` 只约束如何修改本插件，不会自动成为目标项目的规则。

## Skills

- `project-bootstrap`：为新项目建立最小可演化 Harness。先列出将创建的文件，再写入。
- `project-adopt`：把已有项目接入这套工作方式，先理解再最小改造。不要默认改造成插件，也不要默认跑插件 Doctor。
- `root-cause-debug`：证据 -> 假设 -> 最小实验 -> 根因 -> 修复 -> 回归验证。
- `dependency-evaluation`：新增/替换依赖或准备自研通用基础设施时使用。
- `change-review`：先跑预检脚本收集工作区事实（含未跟踪文件 diff），再审查行为、测试证据和未验证项。
- `harness-evolve`：从真实项目的重复摩擦中决定哪些能力应该沉淀、迁移、集成或删除。没有重复证据就停止。
- `harness-doctor`：只检查本插件目录。需要 Python 3.11+；对着业务仓跑会失败。

## Context7 MCP

`mcp.json` 声明 Context7 的远程 Streamable HTTP 服务：

```text
https://mcp.context7.com/mcp
```

插件不保存 API Key。需要更高额度或认证能力时，由当前 Agent 客户端自己的认证机制管理凭证。

## Project Bootstrap Resources

Profile、工程默认值和项目模板属于 `project-bootstrap` Skill 的渐进式资源，而不是自定义顶层协议：

```text
skills/project-bootstrap/
├── SKILL.md
├── references/
│   ├── intake-checklist.md
│   ├── engineering-defaults.md
│   └── profiles/
└── assets/
    ├── AGENTS.repo.template.md
    ├── github/
    └── makefile/
```

`engineering-defaults.md` 是项目规则素材的唯一来源。只有初始化项目时才读取这些内容，并按项目裁剪后写入目标仓库 `AGENTS.md`。

## 能力归属

发现新的限制、规则、工具或专业能力时，不要默认加入 Harness。

```text
New Capability / Constraint
        │
        ▼
是一次性的吗？
   │         │
  是         否
   │         │
Prompt       ▼
         属于当前项目？
          │        │
         是        不确定 / 可能复用
          │        │
          ▼        ▼
    Project Layer  先在真实项目运行
                         │
                    多次重复验证？
                     │         │
                    否         是
                     │         │
                  保持局部      ▼
                          已有成熟能力？
                           │         │
                          是         否
                           │         │
                           ▼         ▼
                      Expert Plugin  再判断是否进入
                      / Tool / MCP   Harness portable core
```

Harness 应优先拥有“怎么做事”的稳定方法，而不是拥有所有“具体怎么实现”的专业知识。

## 与 Expert Plugin 的关系

本插件不声明 Plugin 依赖，也不定义 Plugin-to-Plugin 调用协议。

Developer 领域的专业插件由 Marketplace / Client / Agent Environment 组合使用。例如现代 Go、数据库、安全或前端能力可以作为独立 Expert Plugin 与本 Harness 共存。

Harness 负责通用工作流；Expert Plugin 负责专业能力；Tool / MCP 负责执行或外部知识访问。

## 使用原则

- 项目长期规则进入项目 `AGENTS.md`。
- 特定任务流程进入 Agent Skill。
- 可确定性执行的检查进入项目 Script / Makefile / CI。
- 外部当前知识通过 MCP 或专业插件获取。
- 项目事实保留在项目 Docs / Code / Config。
- 任务状态保留在 Issue / PR / Roadmap。
- 同一类事实只保留一个权威来源。
- 成熟开源能力优先集成，不为“自有”而重复实现。

这套 Harness 通过真实项目持续演化，不追求一次设计完整。实地记录见 [docs/field-tests.md](docs/field-tests.md)。
