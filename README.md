# lookerjin agent market

本仓库是一个面向个人 Agent 工作流的 Codex Marketplace / Distribution 仓库。

目标不是把所有能力塞进一个超级插件，而是维护一组彼此独立、按需安装的 Plugins。Marketplace 只负责发现、分发、组合和版本治理；具体领域由各 Plugin 自己的名称、描述、分类和能力表达。

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
│       ├── .codex-plugin/
│       │   └── plugin.json
│       ├── assets/
│       ├── mcp.json
│       ├── AGENTS.md
│       ├── docs/
│       └── skills/
├── scripts/
│   └── validate_marketplace.py
└── README.md
```

自有插件统一平铺在 `plugins/<plugin-name>/` 下。第三方插件原则上保持其独立仓库，通过 Marketplace remote source 引用，不复制进本仓库。

每个 Codex 插件只保留 `.codex-plugin/plugin.json` 作为 manifest；展示资源统一放在插件根级 `assets/`，由 manifest 使用插件相对路径引用。

## 领域分类

Developer、Creator、Research、Experimental 等领域仍然是有用的认知和治理视图，但不进入物理目录结构，也不新增协议层。

例如：

```text
Developer
├── lookerjin-harness
├── modern-go-guidelines
└── open-code-review-codex

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
- 任务路由与可验证的 Playbook；
- 系统理解、方案探索和项目真实入口验证；
- 根因调试；
- 依赖评估；
- 变更验收与专业审查结果收敛；
- Harness 结构自检、行为评估与演化。

它不承载某门语言或框架的完整专业知识。此类能力优先由独立 Expert Plugin 提供。

软件工程 Harness 的架构图、泳道用户旅程和执行层设计见 [执行层说明](plugins/lookerjin-harness/docs/execution-core.md)。

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

当前 Developer 组合：

| 成员 | 架构角色 | 分工 |
|---|---|---|
| `lookerjin-harness` | 软件工程 Domain Harness | 任务路由、能力组合、行为验收、证据与交付判断 |
| `modern-go-guidelines` | Go Expert Plugin | Go 专业开发指导 |
| `open-code-review-codex` | 专业审查 Plugin | OCR 文件选择、语言规则和缺陷审查；另需可运行的 `ocr` CLI |

OCR 原样引用上游 `plugins/open-code-review`，按用户选择跟随 `main`，具体来源以 Marketplace 清单为准。市场提供可选安装入口，不自动安装 CLI 或调用付费模型；委托模式优先，完整模式按已选择的模型、范围与预算使用。插件包和 CLI 分别更新，刷新后检查入口与实际兼容性；验证记录中的 commit 只表示当次检查对象。领域审查分工与使用边界见 [Change Review 的 OCR 适配](plugins/lookerjin-harness/skills/change-review/references/open-code-review.md)。实际验证见 [field-tests](plugins/lookerjin-harness/docs/field-tests.md)。

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

## 边界

- Marketplace 是分发与组合层；
- Plugin 是能力包边界；
- `Domain Harness`、`Expert Plugin` 是本仓库的架构角色，不是新的协议类型；
- 领域分类是人的视图，不是目录协议；
- 不自定义 Plugin 依赖、继承或 Plugin-to-Plugin 调用协议。

保持结构简单。只有真实使用产生新边界时，才增加新的组织层。
