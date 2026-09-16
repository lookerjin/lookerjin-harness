# lookerjin agent market

本仓库是一个面向个人 Agent 工作流的 Marketplace / Distribution 仓库。

目标不是把所有能力塞进一个超级插件，而是维护一组彼此独立、按需安装的 Agent Plugins。Marketplace 只负责发现、分发、组合和版本治理；具体领域由各 Plugin 自己的名称、描述、分类和能力表达。

## 当前结构

```text
lookerjin-harness/
├── .agents/
│   └── plugins/
│       └── marketplace.json
├── .github/
│   └── workflows/
├── plugins/
│   └── lookerjin-harness/
│       ├── plugin.json
│       ├── mcp.json
│       ├── AGENTS.md
│       ├── docs/
│       └── skills/
├── scripts/
│   └── validate_marketplace.py
└── README.md
```

自有插件统一平铺在 `plugins/<plugin-name>/` 下。第三方插件原则上保持其独立仓库，通过 Marketplace remote source 引用，不复制进本仓库。

## 领域分类

Developer、Creator、Research、Experimental 等领域仍然是有用的认知和治理视图，但不进入物理目录结构，也不新增协议层。

例如：

```text
Developer
├── lookerjin-harness
└── modern-go-guidelines

Creator
├── creator-harness
├── image-generation
└── video-generation

Research
└── research-harness
```

这些分类可以通过 README、Plugin description、keywords、category 等信息表达。Marketplace 本身保持扁平，客户端按需选择和安装具体 Plugin。

## Harness 与专家插件

一个成熟领域可以拥有自己的 Domain Harness。Harness 负责该领域中相对稳定的工作方式，例如如何理解任务、推进流程、验证结果以及什么时候需要专业能力。

Harness 不应该成为领域知识大全。具体语言、框架、工具和创作能力优先由独立 Expert Plugin 提供。

当前 `plugins/lookerjin-harness` 是软件工程领域的 Harness，负责：

- 项目初始化与接入；
- 根因调试；
- 依赖评估；
- 变更审查；
- Harness 自检与演化。

它不承载某门语言或框架的完整专业知识。此类能力优先由独立 Expert Plugin 提供。

## 第三方插件

优先集成成熟、活跃、边界清楚的第三方插件，而不是重复实现。

```text
Marketplace
├── Local Owned Plugin
├── Remote Upstream Plugin
└── Remote Fork Plugin
```

- 原样使用上游：直接通过 Marketplace remote source 引用；
- 需要定制：优先 fork 到独立仓库，再让 Marketplace 指向 fork；
- 只有真正由本仓库维护的插件才放进 `plugins/`。

重要第三方能力应优先固定到经过验证的 ref 或 sha，避免不可控漂移。

## CI 边界

```text
Market
→ 验证 marketplace 组合关系

Local Plugin
→ 验证自己的实现和自测

Remote Plugin
→ 验证远端引用契约

Upstream
→ 负责第三方插件自己的完整测试
```

`.github/workflows/marketplace.yml` 负责 Marketplace 和本地插件检查；`.github/workflows/remote-plugins.yml` 负责远端插件契约巡检。

## 协议边界

- Marketplace 是分发与组合层；
- Plugin 是能力包边界；
- Skills / MCP 是 Agent Plugins 1.0 portable components；
- `Domain Harness`、`Expert Plugin` 是架构角色，不是新的协议类型；
- 领域分类是人的视图，不是目录协议；
- 不自定义 Plugin 依赖、继承或 Plugin-to-Plugin 调用协议。

保持结构简单。只有真实使用产生新边界时，才增加新的组织层。
