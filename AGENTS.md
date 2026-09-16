# lookerjin agent market

本文件只约束 Marketplace 仓库本身的维护方式。具体插件的长期规则由各插件目录内自己的 `AGENTS.md` 负责。

## 仓库定位

- 本仓库是 Agent Plugin 的分发与组合层，不是一个超级插件。
- Marketplace 保持扁平；Developer、Creator、Research、Experimental 等是逻辑分类，不进入物理目录层级。
- 一个成熟领域可以拥有自己的 Domain Harness；Harness 负责领域工作流、判断与验证，不承载所有专业知识。
- 具体语言、框架、工具和创作能力优先由独立 Expert Plugin 提供。
- `Domain Harness` 与 `Expert Plugin` 是架构角色，不是新的 Agent Plugins 协议类型。

## 结构约束

- `.agents/plugins/marketplace.json` 是 OpenAI / Codex Marketplace 分发清单。
- 自有插件平铺在 `plugins/<plugin-name>/` 下，并保持完整、独立的 Plugin 边界。
- 领域分类通过 README、Plugin description、keywords、category 等信息表达，不新增 `plugins/<domain>/` 目录层。
- 第三方插件原则上保持独立来源，通过 Marketplace 引用，不把第三方实现复制进本仓库伪装成自有插件。
- 同一类事实只保留一个权威来源；插件内部规则不要重复抄到仓库根。

## 能力归属

新增能力时依次判断：

1. 它属于什么领域和使用场景；
2. 是否已有成熟、活跃、边界清楚的第三方实现；
3. 是领域级稳定工作流，还是具体专业能力；
4. 是否已经值得成为长期 Marketplace 成员。

优先级：

```text
成熟第三方能力 -> 集成
稳定领域工作流 -> Domain Harness
具体专业能力   -> Expert Plugin
外部执行能力   -> Tool / MCP / App
```

不要为了分类整齐创建空目录、空 Harness 或占位插件。

## 第三方集成

- 优先复用成熟开源，不重复实现已有能力。
- Marketplace 负责来源、组合和版本治理；不要求本仓库拥有底层实现。
- 引入第三方插件前至少确认来源、许可证、维护状态、能力边界和实际可运行性。
- 默认不要跟随不可控的上游漂移；重要第三方能力应优先固定到经过验证的版本、ref 或 sha。
- 原样使用上游时直接 remote 引用；需要长期修改时优先维护独立 fork，而不是复制源码进 Market 仓库。

## 修改规则

- 修改 Marketplace 结构前先核对 OpenAI 当前 Marketplace 行为与 Agent Plugins 当前规范。
- 不新增自定义 Plugin 依赖、继承或 Plugin-to-Plugin 调用协议。
- 不把 OpenAI / Codex 特有分发字段误写成 Agent Plugins portable standard。
- 修改某个插件时，遵守该插件目录内自己的 `AGENTS.md`。
- 修改 `lookerjin-harness` 后运行其 doctor 与相关自测。
- 不提交秘密、令牌或机器专属绝对路径。

## CI 责任

- Marketplace CI 验证清单结构、本地 source 和本地 Plugin 的必要检查。
- Remote Plugin CI 只验证远端引用契约，不接管上游项目完整测试责任。
- 不因为领域分类给 CI 增加额外目录层或路由机制。

## 演化原则

先运行，再根据真实摩擦演化。目录结构优先保持简单，只有真实边界出现时才增加新的组织层。
