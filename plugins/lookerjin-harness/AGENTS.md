# lookerjin-harness

本目录是 `lookerjin-harness` Codex Plugin。AI 是第一消费者，人类文档只是辅助入口。

本文件只约束如何修改这个插件。目标项目的开发原则不写在这里；生成项目规则时只从 `skills/project-bootstrap/references/engineering-defaults.md` 裁剪。

## 结构约束

- `.codex-plugin/plugin.json` 是 Codex 插件身份、版本、展示信息和组件入口的唯一 manifest。
- 根目录不再维护第二份 `plugin.json`，避免名称、版本和描述发生漂移。
- `assets/` 是合法的插件级展示资源目录；logo、composer icon 等由 Codex manifest 使用 `./assets/...` 引用。
- `skills/*/SKILL.md` 是可复用工作流；只在对应任务需要时加载其 `references/`、`scripts/` 和 `assets/`。
- `mcp.json` 声明 MCP 服务；不得提交凭证、API Key 或用户私有配置。
- 不新增自定义顶层 Profile、Hook、Rule、Command 协议；能归属某个 Skill 的资源放进该 Skill。
- Skills 和 MCP 尽量保持客户端无关，但不要为了形式上的“可移植”维护重复 manifest 或自造协议层。

## 修改规则

- 修改 `.codex-plugin/plugin.json` 前先核对 Codex 当前 Plugin / Marketplace 约定。
- 修改任何 Skill 后检查 frontmatter、引用路径和脚本入口。
- 修改插件结构后运行 `python skills/harness-doctor/scripts/doctor.py --root . --json`。
- 能确定性验证的规则优先写成脚本或测试，不只写自然语言要求。
- Manifest 引用的资源必须真实存在；移动 assets、MCP 或 Skills 时同步修改 manifest。
- 不提交秘密、令牌或机器专属绝对路径。
- 同一类事实只保留一个权威来源。

## 有限重试与人工升级

这些规则只适用于维护本插件时的 Agent 行为。

- 不把“完全自主完成”当作目标；目标是自主完成能合理完成的部分，并在外部边界处请求最小人工协助。
- 普通可恢复失败最多尝试 3 次；同类失败连续出现 2 次后，先重新判断根因，不继续无目的变换调用方式撞同一边界。
- 权限不足、平台能力缺失、安全策略拒绝、登录/OAuth、需要用户身份或其他明确外部边界，确认一次后就应停止盲目重试。
- 不为了避免请求用户协助而引入明显更复杂、风险更高或维护成本更大的绕路方案。
- 需要用户协助时必须说明：当前阻塞点、已经验证过什么、用户需要执行的最小具体动作，以及用户完成后 Agent 会继续做什么。

## 演化原则

只把经过真实项目重复验证的流程提升到 Harness。客户端特有能力先按当前客户端约定落地；只有真实使用出现跨客户端需求时，再决定是否抽象额外的可移植层。
