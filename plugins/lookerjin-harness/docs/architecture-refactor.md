# 自适应工程架构与文件职责

本架构以六阶段为主干，以 Track、Mode、Capability 三个独立维度补充路由。每个新增方法必须解决具体决策、执行或验证问题，不增加无独立使用价值的入口。

## 1. 控制与事实归属

| 权威位置 | 拥有内容 | 调用边界 |
|---|---|---|
| `engineering-run/SKILL.md` | 目标→路径、能力组合、回退、交付 | 不内置语言知识、项目启动命令或权限系统 |
| `engineering-run/references/execution-contract.md` | Task / Unit / Evidence / 完成语义、质量底线、沟通与实现的克制 | Change Review 与项目规则生成引用同一处；不创建独立契约 Skill |
| `engineering-run/references/lifecycle.md` | 六阶段进入、跳过、退出、回退与反馈入口 | 阶段不强制产物，不定义第二套任务队列 |
| `engineering-run/references/tracks-and-modes.md` | 四类验收与四类可组合执行方式 | Prototype / Long Run 不再伪装任务类型 |
| `engineering-run/references/collaboration.md` | 人与 Agent 的决策、观察、授权协作 | 必需回答阻塞相关 Unit，独立任务继续 |
| `engineering-run/references/continuity.md` | 检查点、实际工作区恢复、证据失效与历史事实版本 | 复用现有项目状态位置，不另建知识库 |
| `help/SKILL.md` | 用法解释、场景推荐、宿主入口与能力发现 | 只问用法不启动实施；按问题读框架或已知专家元数据 |
| `system-understand/references/code-navigation.md` 与 `scripts/code-map.py` | 文本/符号/结构选路、局部 JSON 与 draw.io、内容新鲜度 | 按范围提取、固定输入、原子发布；不安装后台索引 |
| `engineering-run/references/ui-capabilities.md` | UI 专家选择、设计与真实交互验证 | 已启用能力按需使用，小修不强制重新设计 |
| `root-cause-debug/references/feedback-loop.md` | 原症状复现、区分实验、输入缩减与同入口复验 | 记录反馈耗时和复现率，不以偶然通过作为修复 |
| `harness-eval/references/protocol.md` | 固定判据、独立配对、统一复验、质量/耗时/可观测成本 | 分派前计时，自报与事实分开；缺失费用不估造 |
| 项目规则、代码、配方、Issue / PR | 实际产品事实、命令、验收与当前状态 | 插件保存方法，项目保存事实 |

所有路径相对 `skills/`。基础契约保留在现有拥有者目录，评估工具仍可完整注入 `skills/`；避免为了形式分层增加插件级共享资源协议。

Harness 内有 15 个 Skill。独立 UI 专家位于仓库的 `plugins/frontend-design/skills/frontend-design/SKILL.md`，分发记录与许可证留在该插件。Marketplace 共 4 个成员，声明位于 `.agents/plugins/marketplace.json`；发现、安装与启用由宿主负责。主 Agent 根据任务组合能力，不存在自动 Plugin-to-Plugin 调用协议。

## 2. 六阶段的具体方法

| 阶段 | 本阶段动作 | 被调用能力与产物 | 失败或不适用时 |
|---|---|---|---|
| Brainstorm | 查现成事实，识别目标/范围/验收歧义，建立决定依赖 | Decision Dialogue；会话决定或已有计划中的更新 | 已知目标直接跳过；用户更改目标重算问题 |
| Design | 追真实入口、状态、所有权；比较结构不同方案；实验关键假设 | System Understand / Design Explore / Dependency Evaluation；必要 ADR | 小改不比赛方案；假设失败回到候选与边界 |
| Plan | 按纵向行为拆 Unit，设依赖、写入范围、验收、验证、预算 | 可选计划导出与 check-plan.py；先选代表性 pilot | 单步在会话表达；环依赖重拆，不随机选工作 |
| Execute | 可验证切片；兼容迁移按扩展→迁移→收缩；明确写入所有者 | 现有专业能力 / Root Cause Debug；产品 diff | 因机制未知停止猜修；必要时回 Design |
| Verify | 正确实例→真实入口→输出和副作用→清理保留证据；覆盖回归和集成 | Verification Run / 项目配方 / Change Review；逐项证据 | 实现错回 Execute；模型错回 Design；阻塞记未验证 |
| Ship | 核对最终产物与证据、既有质量门槛、交付目标和授权 | 可交接 / commit / push / PR / deploy / release | 有缺口只能部分交付；现实反馈重新路由 |

质量保证按风险增加失败路径、负对照、兼容验证、独立审查或形式化检查；不能通过多写阶段文档替代证明。

## 3. 决策追问

`decision-dialogue/SKILL.md` 拥有方法入口，`references/frontier.md` 拥有算法。

1. 范围内先自行核对仓库事实，复用用户已给答案。
2. 问题记录前置、证据、推荐、后果和状态。
3. 取全部前置已解决的未决问题作为当前前沿；根据客户端容量分批呈现，不设任意总轮数。
4. 等待必需回答，同时推进独立工作；回答改变前提后删除失效问题、重算前沿。
5. 局部澄清在阻塞解除后返回阶段；完整追问要求关键前沿清空和共同理解确认。用户中止则交付剩余未知。

只在术语歧义影响实现时保存领域词汇，只在长期取舍需要动机时保存 ADR。人工观察沿用 Collaboration，不误当作产品决定或外部授权。

## 4. 验证的建立、运行与维护

| 职责 | 文件 | 实际退出条件 |
|---|---|---|
| Bootstrap | `verification-bootstrap/SKILL.md` 与 `references/recipe-shape.md` | 复用或修复唯一项目配方；至少一条真实代表路径；未跑标 draft |
| Run | `verification-run/SKILL.md` | 本任务影响面逐项核对入口、返回、错误与副作用，证据清理后保留 |
| Maintain | `verification-run/references/maintenance.md` | 比较成功基线后的入口、状态写入者与承诺；完整声明覆盖运行后才推进同步基线 |
| Formal checks | `verification-run/references/formal-checks.md` | 代码到模型映射、版本/边界/假设、实际检查、负对照、反例与产品复现边界 |
| Evidence | `verification-run/references/evidence-format.md` 与 `scripts/check-evidence.py` | 必要 ID 齐全，声明状态符合要求，源码/配置/产物和日志指纹仍一致；不判定语义真实性 |

Run 缺配方时报告给调用方选择 Bootstrap，不互相递归。Maintain 的 updated 与 bug-found 可以同时存在，blocked 不推进成功基线。形式化能力按项目与工具提供，不内置大型建模运行时。

## 5. 执行与恢复

每个 Unit 保留 goal、scope、context、acceptance、verify、depends_on、status；完成需 evidence，阻塞需 blocker。`check-plan.py` 检查字段、未知依赖、重复、循环及提前开始，返回 ready 和同名范围重叠信号。它不推断隐藏依赖，也不调度工作。

Long Run 先 pilot 再扩大；Parallel 先隔离写入；Subagent 需宿主允许，交付原始证据并由负责人复核。整体完成还要集成验收。

恢复核对真实分支、未提交修改、资源和授权；根据验收依赖决定证据是否失效。历史知识保留观察日期与源码状态，不能让摘要覆盖现在的事实。所有记录使用项目已有位置。

## 6. 工具、hooks 与权限

| 已落地机制 | 执行方式 | 可证明的边界 |
|---|---|---|
| 计划依赖检查 | Python 标准库 CLI，显式调用 | 记录结构与显式依赖 |
| 证据有效性检查 | Python 标准库 CLI，显式调用 | 必要 ID、状态、相对路径、实际文件哈希 |
| 插件自检 | Doctor + 自测 + Marketplace CI | 发现入口、资源引用、目录一致性、Python 语法与负例诊断 |
| 私有演化入口 | SKILL 显式触发描述与 `agents/openai.yaml` | 元数据存在且一致；运行是否尊重由宿主负责 |
| 可恢复执行 | 项目现有状态与会话恢复流程 | 由 Agent 核对真实状态；未宣称后台自动恢复 |
| 局部代码导航 | `system-understand/scripts/code-map.py`，按需调用解析器 | 同一关系集查询/出图，固定输入与发布前复核；语义仍需源码或运行核对 |
| UI 设计与验收 | 独立 Frontend Design + 项目浏览器/验证配方 | 视觉方向、交互、键盘/焦点、窄屏、真实渲染对比度分别验收 |
| 分发校验 | 仓库 `scripts/validate_marketplace.py` 与 `frontend_design_test.py` | manifest 内容/名称、资源路径、固定正文与许可证；安装链路另行实测 |

本版本不引入 hooks、命令拦截或后台索引；需要的检查通过显式 CLI 与 CI 执行。沟通、实现与审查共享执行契约，禁止防御性表达和无实际依据的防御型编程。

## 7. 私有演化与验证范围

仅显式用户请求进入 Evidence → Eval → Distill → Evolve → Doctor，交付与错误不会自动触发。用户主动设计可以成为候选实施；跨项目收益仍需真实重复证据。

检查结果按版本保留在 [field-tests](field-tests.md)：包括生命周期配对行为、Help 与入口、导航失效/并发、调试反馈，以及 [UI 配对试验](frontend-design-ab.md) 的共同浏览器复验和 CLI 安装链路。脚本自测证明机械行为，Doctor 证明结构；单次配对结果不外推为跨项目、跨客户端的稳定收益。每轮缺失的计时、费用或运行场景在各自记录中标明。

## 8. 演进与阅读入口

- 删除 `engineering-run/references/playbooks/` 六份旧流程，其方法归入 lifecycle 与 tracks-and-modes。
- 保留共用 execution-contract 与 recipe-shape 原路径；已安装 Skill-only 副本保留资源闭包。
- 生命周期重构时新增 Decision Dialogue、Verification Run，后续新增 Help；当前共 15 个。维护、契约、六阶段都不单独成为 Skill。
- 导航方法与脚本归 System Understand；UI 专家归独立插件；简洁表达和实现克制归共同执行契约。
- 更新 Change Review、Root Cause Debug、项目接入与私有演化接口；确定性检查加入同一 CI。
- 原生图分别见 [架构](architecture-refactor.drawio) 与 [用户旅程](user-journey.drawio)，实际结果见 [field-tests](field-tests.md)。
