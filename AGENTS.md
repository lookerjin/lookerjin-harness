# lookerjin agent market

本文件只约束 Marketplace 仓库本身的维护方式。具体插件的长期规则由各插件目录内自己的 `AGENTS.md` 负责。

## 仓库定位

- 本仓库是 Agent Plugin 的分发与组合层，不是一个超级插件。
- 按领域组织能力，例如 Developer、Creator、Research、Experimental。
- 一个成熟领域可以拥有自己的 Domain Harness；Harness 负责领域工作流、判断与验证，不承载所有专业知识。
- 具体语言、框架、工具和创作能力优先由独立 Expert Plugin 提供。
- `Domain Harness` 与 `Expert Plugin` 是架构角色，不是新的 Agent Plugins 协议类型。

## 结构约束

- `.agents/plugins/marketplace.json` 是 OpenAI / Codex Marketplace 分发清单。
- 自有插件放在 `plugins/<domain>/<plugin-name>/` 下，并保持完整、独立的 Plugin 边界。
- 第三方插件原则上保持独立来源，通过 Marketplace 引用，不把第三方实现复制进本仓库伪装成自有插件。
- 不为了目录完整提前创建空领域、空 Harness 或占位插件。
- 同一类事实只保留一个权威来源；插件内部规则不要重复抄到仓库根。

## 能力归属

新增能力时依次判断：

1. 属于哪个领域；
2. 是否已有成熟、活跃、边界清楚的第三方实现；
3. 是领域级稳定工作流，还是具体专业能力；
4. 如果只是实验性能力，先保持实验状态，不急于提升为 Domain Harness 或 Core 能力。

优先级：

```text
成熟第三方能力 -> 集成
稳定领域工作流 -> Domain Harness
具体专业能力   -> Expert Plugin
外部执行能力   -> Tool / MCP / App
```

## 第三方集成

- 优先复用成熟开源，不重复实现已有能力。
- Marketplace 负责来源、组合和版本治理；不要求本仓库拥有底层实现。
- 引入第三方插件前至少确认来源、许可证、维护状态、能力边界和实际可运行性。
- 默认不要跟随不可控的上游漂移；重要第三方能力应优先固定到经过验证的版本或 ref。

## 修改规则

- 修改 Marketplace 结构前先核对 OpenAI 当前 Marketplace 行为与 Agent Plugins 当前规范。
- 不新增自定义 Plugin 依赖、继承或 Plugin-to-Plugin 调用协议。
- 不把 OpenAI / Codex 特有分发字段误写成 Agent Plugins portable standard。
- 修改某个插件时，遵守该插件目录内自己的 `AGENTS.md`。
- 修改 Developer Harness 后运行其 doctor 与相关自测。
- 不提交秘密、令牌或机器专属绝对路径。

## 演化原则

先运行，再根据真实摩擦演化。

只有当一个领域已经出现稳定工作流、重复判断和多个专业能力需要协调时，才新增 Domain Harness。只有经过实际验证的第三方能力才进入长期 Marketplace 组合。
