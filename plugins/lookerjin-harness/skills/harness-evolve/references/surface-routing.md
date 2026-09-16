# Harness Surface Routing

遇到新规则、流程、事实或工具时，先判断它属于哪一层，不要先问“放哪个文件”。

| 内容 | 默认承载面 | 判断 |
|---|---|---|
| 跨项目、跨客户端仍成立的任务流程 | `skills/` | 只在某类任务触发 |
| 生成项目时可选用的工程原则 | `project-bootstrap/references/engineering-defaults.md` | 裁剪后写入项目 `AGENTS.md` |
| 项目始终成立的规则 | `<repo>/AGENTS.md` | 项目内大多数任务都应知道 |
| 本插件仓库的维护规则 | 插件根目录 `AGENTS.md` | 只约束如何修改本仓库 |
| 项目领域事实、架构、契约 | Docs / code / config | 描述系统是什么 |
| 当前开发状态 | Issue / PR / Roadmap | 描述现在做到哪 |
| 可重复命令和门禁 | Script / Makefile / CI | 应确定性执行 |
| 外部库当前文档 | Context7 / 官方文档 / Web | 不复制成长期项目事实 |
| 外部系统数据与动作 | MCP | 让工具做真实交互 |
| 仅对某个客户端成立的 Hook / Command / 权限 | reverse-domain client extension | 不进 portable core |
| 一次性任务要求 | 当前 Prompt / Thread | 不污染长期配置 |

## 判断顺序

1. 这是事实还是过程？
2. 是否每个任务都需要知道？
3. 是否只在一个项目成立？
4. 能不能机械验证或机械禁止？
5. 是否依赖外部实时状态？
6. 是否已经存在权威来源？
7. 换一个 Agent 客户端后还成立吗？

## 避免

- 把整个项目需求复制进 Skill。
- 同一规则同时维护在 AGENTS、Skill 和 README。
- 为客户端本来就会的通用常识创建 Skill。
- 把 Hook 写成 portable Skill 的默认步骤。
- 用模型提示词替代本来可以脚本化的验证。
- 对业务仓库运行本插件的 Doctor。
