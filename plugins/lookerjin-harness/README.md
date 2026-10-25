# lookerjin-harness

软件工程 Domain Harness：由目标决定路径，用实际证据判断结果。以 Codex Plugin 分发，具体语言、框架与专业工具由可用专家能力提供。

## 怎么开始

直接描述目标、必要约束和完成标准即可，例如：“先讨论这个模块怎么拆，保留对外行为，方案定下来前先不实现。”无需先输入总控命令或手动选择六阶段。

不确定怎么用时，问“这个 Harness 怎么用？”或“我想重构这个模块，该怎么开始？”。[help](skills/help/SKILL.md) 会读取当前安装的相关说明，解释推荐路径并给一条可直接发送的示例。也可以从客户端技能列表选择“help / Harness 帮助”；具体调用方式以宿主为准，裸 `/help` 可能是客户端内置命令。单纯问用法不会启动开发或演化流程，明确要求执行时则继续对应工作。

日常只需记住两种入口：

| 想做什么 | 直接发送 |
|---|---|
| 问用法、找适合的路径 | “我想了解这个项目，该怎么用 Harness？” |
| 开始或继续工作 | “看一下这个模块的调用关系，给我图和风险；先别改代码。” |

也可以直接说“解释这个问题，然后修好并验证”，Agent 应在必要解释后继续执行，不要求你再发一次命令。若已知道所需专业技能，可按客户端提供的方式直接选择，完整目录仍在下方。

通用入口依靠自然语言和技能正文，不依赖专属斜杠别名或菜单隐藏。支持技能菜单的客户端使用真实列出的入口；只有文件读取能力的客户端，可以读取已安装的 `SKILL.md` 及必要引用。展示元数据是可选增强。当前仓库仍以 Codex Plugin 分发；这些通用用法不代表所有客户端都能直接安装该包，安装与自动发现须由对应宿主验证。

## 自适应六阶段

Brainstorm → Design → Plan → Execute ⇄ Verify → Ship。

六阶段是 `engineering-run` 的内部状态，不是六个 Skill，也不是六个必须生成的文件。已知小改可以直接 Execute → Verify；架构重构先固定行为契约，再设计职责、拆依赖、分步迁移与集成验证。验证发现假设错误可以回 Design；只要方案或原型时按约定产物交付。

| 维度 | 职责 |
|---|---|
| Lifecycle | 当前要解决的阶段问题，允许跳过与回退 |
| Track | Feature / Bug Fix / Refactor / Investigate 的验收语义 |
| Mode | 按需组合 Prototype / Long Run / Parallel / Subagent |
| Capability | 领域 Skill、专家、Human、MCP 与工具的实际能力 |

人和 Agent 可以双向委托：关键决定使用依赖就绪的追问，真人观察或操作更有效时提出最小请求，同时推进独立工作。Ship 是约定交付状态，可为可交接、commit、push、PR、部署或发布；已有授权继续有效。

## 能力目录

| Skill | 何时调用 |
|---|---|
| [help](skills/help/SKILL.md) | 解释 Harness 用法、场景选路与运行边界，按需读取当前技能说明 |
| [engineering-run](skills/engineering-run/SKILL.md) | 跨步骤任务推进、路径选择、阶段回退与交付 |
| [decision-dialogue](skills/decision-dialogue/SKILL.md) | 用户掌握的信息决定目标或方案，或用户明确要求完整追问 |
| [system-understand](skills/system-understand/SKILL.md) | 追踪真实入口、状态、所有权和约束；按需查询局部代码关系并导出 draw.io |
| [design-explore](skills/design-explore/SKILL.md) | 有实质结构差异的方案选择与关键假设实验 |
| [project-bootstrap](skills/project-bootstrap/SKILL.md) | 新项目建立必要工程规则与门禁 |
| [project-adopt](skills/project-adopt/SKILL.md) | 既有项目保留约定，只补实际缺口 |
| [verification-bootstrap](skills/verification-bootstrap/SKILL.md) | 创建或修复项目配方，证明代表性路径可用 |
| [verification-run](skills/verification-run/SKILL.md) | 按真实入口执行验证；显式维护完整声明覆盖面 |
| [root-cause-debug](skills/root-cause-debug/SKILL.md) | 复现、竞争假设、区分实验、机制与同入口复验 |
| [dependency-evaluation](skills/dependency-evaluation/SKILL.md) | 依赖适用性、版本与运行成本评估 |
| [change-review](skills/change-review/SKILL.md) | 实际 diff、质量底线、专业发现与证据适用性收敛 |
| [harness-eval](skills/harness-eval/SKILL.md) | 隔离快照、固定判据、比较实际行为 |
| [harness-evolve](skills/harness-evolve/SKILL.md) | 仅用户明确要求时提炼、改变自身工作方法 |
| [harness-doctor](skills/harness-doctor/SKILL.md) | 本插件结构、活跃引用、入口元数据与脚本语法检查 |

15 个 Skill。共用契约仍归 Engineering Run 的 references，验证配方形状仍归 Verification Bootstrap；调用方引用同一份资源。配方维护是 Verification Run 的显式路径，未增加独立入口。

## 具体方法与文件

- [执行契约](skills/engineering-run/references/execution-contract.md)：目标、授权、事实标签、证据状态、质量底线与完成条件。
- [生命周期](skills/engineering-run/references/lifecycle.md) 与 [Track / Mode](skills/engineering-run/references/tracks-and-modes.md)：选路、跳过、回退、兼容迁移、pilot 与 Unit。
- [协作](skills/engineering-run/references/collaboration.md) 与 [连续性](skills/engineering-run/references/continuity.md)：最小人工请求、独立推进、基线核对和恢复。
- [决策前沿](skills/decision-dialogue/references/frontier.md)：先查事实、只问前置已满足的问题、回答后重算。
- [配方维护](skills/verification-run/references/maintenance.md) 与 [形式化检查](skills/verification-run/references/formal-checks.md)：覆盖漂移、新写入者、成功同步基线、模型负对照与真实入口边界。
- [计划检查器](skills/engineering-run/scripts/check-plan.py) 与 [证据检查器](skills/verification-run/scripts/check-evidence.py)：可选 JSON 导出上的确定性检查，不另建运行引擎或状态数据库。
- [代码导航](skills/system-understand/references/code-navigation.md)：按问题选文本/符号/结构查询，局部关系 JSON 与 draw.io 同源；内容指纹识别过期。JS 模块依赖可选接入固定版本解析工具，其他语言复用已有工具和源码证据，不默认安装全库索引。
- [调试反馈闭环](skills/root-cause-debug/references/feedback-loop.md)：先建立能命中原症状的反馈，记录耗时/复现率、逐项缩减输入，修复后重跑原始路径。代码导航在固定输入副本上提取关系，完整暂存后原子创建输出，失败与并发不覆盖已有产物。
- [UI 能力接入](skills/engineering-run/references/ui-capabilities.md)：设计、组件实现、规则检索与真实界面验证按需组合，沿用六阶段；专家尚未安装时不宣称可用。候选与实际试验见 [UI 评估](docs/ui-capability-evaluation.md)。
- [评估协议](skills/harness-eval/references/protocol.md)：同时比较完成质量、耗时与可观测成本，分别报告准备、执行、重试与未知的模型计费。

这些是按需加载的方法。本版本不引入 hook、会话后台脚本或命令拦截器，检查器由任务显式调用或在 CI 运行。私有演化入口同时声明显式调用元数据，实际执行仍受宿主支持与授权约束。

## 运行与验证

Python helper 使用 Python 3.11+ 标准库。在插件根运行：

```bash
python skills/harness-doctor/scripts/doctor.py --root . --json
python skills/engineering-run/scripts/check-plan_test.py
python skills/verification-run/scripts/check-evidence_test.py
python skills/harness-doctor/scripts/doctor_test.py
python skills/change-review/scripts/preflight_test.py
python skills/project-bootstrap/scripts/check-placeholders_test.py
python skills/harness-eval/scripts/prepare_test.py
python skills/system-understand/scripts/code-map_test.py
```

JSON 输入格式分别见 [计划输入](skills/engineering-run/references/plan-format.md) 与 [证据输入](skills/verification-run/references/evidence-format.md)。检查器通过不证明 Agent 实际遵循流程，也不证明产品行为正确；实际运行结果与边界见 [field-tests](docs/field-tests.md)。

代码导航本地自测默认运行标准库部分；设置 `DEPCRUISE` 为已安装的 CLI 路径时，同时运行真实解析器的两项集成测试。CI 在临时工具目录安装固定版本并运行全部导航测试。可查看 [初版检查](docs/code-navigation-checks.json)、[故障与并发加固记录](docs/method-hardening-checks.json) 与 [本实现的局部调用图](docs/code-navigation.drawio)。

## 包与文档

`.codex-plugin/plugin.json` 是唯一 manifest，`skills/` 为发现入口，`assets/` 存放展示资源，`mcp.json` 配置 Context7。MCP 是否可用由当前客户端和服务决定，不把插件声明当成调用成功。

详细文件职责与迁移见 [架构说明](docs/architecture-refactor.md)，入口说明见 [execution-core](docs/execution-core.md)。两张原生 draw.io 图分别为 [架构图](docs/architecture-refactor.drawio) 与 [用户旅程图](docs/user-journey.drawio)。
