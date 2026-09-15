# lookerjin-harness

一个面向 AI Coding Agent 的个人软件工程插件，按 Agent Plugins 1.0 组织。

核心目标是把跨项目可复用的工程方法沉淀成可移植 Skills，把外部文档能力通过 MCP 提供；平台特有能力只作为可选扩展，不进入 portable core。

## 安装

推荐直接把仓库地址交给 Agent：

```text
https://github.com/lookerjin/lookerjin-harness
```

然后告诉它：

```text
安装这个 Agent Plugin，并验证 skills 和 MCP 是否可用。
如果当前客户端不原生支持 Agent Plugins 1.0，就按 plugin.json、skills/ 和 mcp.json 的标准结构适配到当前客户端；不要修改 portable core。
```

支持 Agent Plugins 的客户端应从根目录发现：

```text
plugin.json   -> 插件身份与规范版本
skills/       -> Agent Skills
mcp.json      -> MCP Servers
```

### OpenAI / Codex

仓库同时提供 `.agents/plugins/marketplace.json` 作为 OpenAI / Codex 的分发适配层。它只把仓库根目录注册为插件，仍然直接复用 `plugin.json`、`skills/` 和 `mcp.json`，不维护第二套插件定义。

从 GitHub 导入 marketplace 时使用仓库根地址，Path 留空；需要测试非默认分支时，在导入界面选择对应 branch、tag 或 commit。

## 架构

```text
lookerjin-harness/
├── plugin.json
├── mcp.json
├── AGENTS.md
├── docs/                       # 仓库文档与 field-test 证据
├── .agents/
│   └── plugins/
│       └── marketplace.json   # OpenAI / Codex distribution adapter
└── skills/
    ├── project-bootstrap/
    ├── project-adopt/
    ├── root-cause-debug/
    ├── dependency-evaluation/
    ├── change-review/
    ├── harness-evolve/
    └── harness-doctor/
```

Agent Plugins 1.0 的 portable component 只有 Skills 和 MCP Servers。本仓库不自定义第三套插件协议。

`docs/` 只是仓库级文档和实地验证记录，不是 Agent Plugins component，也不参与插件发现。Agent Plugins 1.0 只规定标准组件的固定发现位置，并不要求插件根目录只能包含这些文件。

`.agents/plugins/marketplace.json` 不是 portable component，只是 OpenAI / Codex 的分发清单；它只引用仓库根插件，不复制或改变 portable core 的语义。

根目录 `AGENTS.md` 只约束如何修改本插件，不会自动成为目标项目的规则。

## Skills

- `project-bootstrap`：为新项目建立最小可演化 Harness。先列出将创建的文件，再写入。
- `project-adopt`：把已有项目接入这套工作方式，先理解再最小改造。不要默认改造成插件，也不要默认跑插件 Doctor。
- `root-cause-debug`：证据 -> 假设 -> 最小实验 -> 根因 -> 修复 -> 回归验证。
- `dependency-evaluation`：新增/替换依赖或准备自研通用基础设施时使用。
- `change-review`：先跑预检脚本收集工作区事实（含未跟踪文件 diff），再审查行为、测试证据和未验证项。
- `harness-evolve`：从真实项目的重复摩擦中决定哪些能力应该沉淀、迁移或删除。没有重复证据就停止。
- `harness-doctor`：只检查本插件仓库。需要 Python 3.11+；对着业务仓跑会失败。

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

## 规则放置与演化

发现新的限制、规则或工作方式时，先判断作用域、生命周期和是否需要机械保证，不要直接写进 portable core。

```text
New Rule / Constraint
        │
        ▼
这是一次性的吗？
   │         │
  是         否
   │         │
Prompt       ▼
         属于当前项目？
          │        │
         是        不确定 / 可能通用
          │        │
          ▼        ▼
    Project Layer  先在项目运行
          │              │
          │         多次重复验证？
          │          │         │
          │         否         是
          │          │         │
          │        保持局部     ▼
          │                harness-evolve
          │                     │
          ▼                     ▼
     类型是什么？          Portable Core
          │
  ┌───────┼────────┬─────────────┐
  ▼       ▼        ▼             ▼
规则     流程      事实          机械约束
项目AGENTS  Skill   Docs/Code   Script/CI
```

再额外判断一次：

```text
如果明天换一个 Agent，这条规则还有意义吗？

有   -> 保持在项目层或 portable core
没有 -> 放到对应 Client Extension / Adapter
```

推荐的晋升路径：

```text
Prompt
  ↓
Project Rule / Project Skill / Project Script
  ↓
Repeated Evidence
  ↓
harness-evolve
  ↓
Portable Core
```

不要跳级。已经进入 portable core 的能力如果后来发现只适用于某类项目、某个平台或已经失效，也应该降级、迁移或删除。

## 平台适配

`plugin.json`、`skills/` 和 `mcp.json` 构成跨 Agent 的 portable core。

如果未来某个客户端确实需要专属运行能力，例如 Hook 或客户端权限配置，再按 Agent Plugins 1.0 的 Client Extensions 机制隔离实现；没有真实需求时不提前创建客户端专属扩展。

当前仓库的 `.agents/plugins/marketplace.json` 仅用于 OpenAI / Codex 发现和分发插件，不属于 portable core，也不会改变插件运行语义。

## 使用原则

- 项目长期规则进入项目 `AGENTS.md`。
- 特定任务流程进入 Agent Skill。
- 可确定性执行的检查进入项目 Script / Makefile / CI。
- 外部当前知识通过 MCP 获取。
- 项目事实保留在项目 Docs / Code / Config。
- 任务状态保留在 Issue / PR / Roadmap。
- 同一类事实只保留一个权威来源。

这套插件通过真实项目持续演化，不追求一次设计完整。实地记录见 [docs/field-tests.md](docs/field-tests.md)。
