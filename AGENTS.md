# lookerjin-harness

本仓库是一个符合 Agent Plugins 1.0 的可移植个人软件工程插件。AI 是第一消费者，人类文档只是辅助入口。

本文件只约束如何修改这个插件仓库。目标项目的开发原则不写在这里；生成项目规则时只从 `skills/project-bootstrap/references/engineering-defaults.md` 裁剪。

## 结构约束

- `plugin.json` 是插件身份与 Agent Plugins 版本的唯一标准清单。
- `skills/*/SKILL.md` 是可移植工作流；只在对应任务需要时加载其 `references/`、`scripts/` 和 `assets/`。
- `mcp.json` 只声明可移植 MCP；不得提交凭证、API Key 或用户私有配置。
- 平台特有内容必须放在反向域名命名的顶层扩展目录，不能污染 portable core。
- 不新增自定义顶层 Profile、Hook、Rule、Command 协议；能归属某个 Skill 的资源放进该 Skill。

## 修改规则

- 修改标准结构前先核对 Agent Plugins / Agent Skills / MCP 当前规范。
- 修改任何 Skill 后检查 frontmatter、引用路径和脚本入口。
- 修改插件结构后运行 `python skills/harness-doctor/scripts/doctor.py --root . --json`。
- 能确定性验证的规则优先写成脚本或测试，不只写自然语言要求。
- 不把某个 Agent 客户端的配置误写成跨平台标准。
- 不提交秘密、令牌或机器专属绝对路径。
- 同一类事实只保留一个权威来源。

## 有限重试与人工升级

这些规则只适用于维护本仓库时的 Agent 行为。

- 不把“完全自主完成”当作目标；目标是自主完成能合理完成的部分，并在外部边界处请求最小人工协助。
- 普通可恢复失败最多尝试 3 次；同类失败连续出现 2 次后，先重新判断根因，不继续无目的变换调用方式撞同一边界。
- 权限不足、平台能力缺失、安全策略拒绝、登录/OAuth、需要用户身份或其他明确外部边界，确认一次后就应停止盲目重试。
- 不为了避免请求用户协助而引入明显更复杂、风险更高或维护成本更大的绕路方案。
- 需要用户协助时必须说明：当前阻塞点、已经验证过什么、用户需要执行的最小具体动作，以及用户完成后 Agent 会继续做什么。

## 演化原则

只把经过真实项目重复验证的流程提升到 portable core。客户端特有能力先作为 adapter 验证，只有形成跨客户端稳定契约后才考虑提升。
