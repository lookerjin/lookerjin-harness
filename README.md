# lookerjin agent market

本仓库是一个面向个人 Agent 工作流的 Marketplace / Distribution 仓库。

目标不是把所有能力塞进一个超级插件，而是按领域组合独立插件：每个成熟领域可以有自己的 Harness 负责该领域的工作流、判断与验证，再由专家插件提供更具体的语言、框架、工具或创作能力。

## 当前结构

```text
lookerjin-harness/
├── .agents/
│   └── plugins/
│       └── marketplace.json
├── .github/
│   └── workflows/
├── plugins/
│   └── developer/
│       └── lookerjin-harness/
│           ├── plugin.json
│           ├── mcp.json
│           ├── AGENTS.md
│           ├── docs/
│           └── skills/
└── README.md
```

当前只有 `Developer` 领域已经形成稳定 Harness，因此只创建实际存在的目录，不提前创建 Creator、Research 或 Experimental 的空壳。

## 领域模型

```text
Marketplace
├── Developer
│   ├── Domain Harness
│   └── Expert Plugins
├── Creator
│   ├── Domain Harness
│   └── Expert Plugins
├── Research
│   ├── Domain Harness
│   └── Expert Plugins
└── Experimental
    └── 尚未形成稳定工作流的实验能力
```

领域是组织和治理概念，不是新的 Agent Plugins 协议类型。

### Domain Harness

Domain Harness 负责该领域中相对稳定的工作方式，例如：

- 如何理解任务与上下文；
- 如何推进工作流；
- 如何验证结果；
- 什么时候需要调用专业能力；
- 什么时候应该停止扩大范围。

Harness 不应该成为领域知识大全。

### Expert Plugin

专家插件负责具体专业能力，例如：

- Developer：Go、Python、TypeScript、数据库、安全、前端等；
- Creator：图像生成、视频生成、剪辑、配音、发布等；
- Research：检索、论文阅读、资料分析等。

优先集成成熟、活跃、边界清楚的第三方插件，而不是重复实现。第三方插件原则上保持独立来源，由 Marketplace 负责发现、组合和版本治理，不复制进本仓库成为自有实现。

## 当前 Developer Harness

`plugins/developer/lookerjin-harness` 是当前已有的软件工程 Domain Harness。

它负责通用 AI Coding 工程流程，包括：

- 项目初始化与接入；
- 根因调试；
- 依赖评估；
- 变更审查；
- Harness 自检与演化。

它不负责承载某门语言或某个框架的完整专业知识。此类能力应优先由独立 Expert Plugin 提供。

## 演化原则

新增能力时按下面顺序判断：

```text
新能力 / 重复摩擦
      ↓
属于哪个领域？
      ↓
是否已经存在成熟第三方能力？
   ┌──┴──┐
   是     否
   ↓       ↓
优先集成   再判断是否值得自研
      ↓
它是领域工作流，还是具体专业能力？
   ┌──────────┴──────────┐
   ↓                     ↓
Domain Harness       Expert Plugin
```

只有当一个领域出现稳定工作流、重复判断和多个专业能力需要协调时，才创建对应 Domain Harness。

## OpenAI / Codex

`.agents/plugins/marketplace.json` 是 OpenAI / Codex 的 Marketplace 分发清单。

本仓库中的自有插件使用本地子目录作为 source；未来引入第三方插件时优先引用其独立 GitHub 来源，不复制第三方实现。

## 协议边界

- Marketplace 是分发与组合层；
- Plugin 是能力包边界；
- Skills / MCP 是 Agent Plugins 1.0 portable components；
- `Domain Harness`、`Expert Plugin` 是本仓库的架构角色，不是新的协议类型；
- 不自定义 Plugin 依赖、Plugin 继承或 Plugin-to-Plugin 调用协议。

先通过真实使用验证，再扩展结构。不要为了目录完整提前创建没有实际能力的领域或插件。
