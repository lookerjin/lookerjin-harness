# 自适应执行核心

Engineering Run 将目标、验收与已有授权映射为最短充分路径。六阶段允许跳过、回退和局部交付；领域能力按需调用，专业能力通过当前客户端接入。

日常入口是“问用法”和“直接说目标”，分别由 Help 和适合当前任务的技能处理；窄任务可直接进入专业技能，跨步骤任务由 Engineering Run 推进。[入口行为](../skills/help/SKILL.md) 包含自然语言、宿主技能调用和已安装文件读取的适配边界，不新增斜杠别名协议。

- [架构与具体文件职责](architecture-refactor.md)
- [架构图：原生 draw.io](architecture-refactor.drawio)
- [用户旅程：原生 draw.io](user-journey.drawio)
- [本项目运行记录](field-tests.md)

## 运行边界

共同执行契约属于 `engineering-run/references`，调用它只加载资源，不额外调用一个“契约 Skill”。Track 不各自维护一套阶段，Mode 不取代目标。人提供决定或观察时 Agent 继续独立工作。

沟通与实现按 [执行契约](../skills/engineering-run/references/execution-contract.md#沟通与实现的克制) 收敛：简洁表达；校验、重试和恢复对应实际边界；Change Review 检查重复防御与掩盖错误的兜底。项目规则生成也从同一处裁剪。

代码关系问题先选 `rg`、符号查询或局部结构提取；需要图时使用 [代码导航](../skills/system-understand/references/code-navigation.md)，输出同源 JSON / draw.io，并检查内容指纹。UI 设计按 [能力接入](../skills/engineering-run/references/ui-capabilities.md) 使用已启用的独立 Frontend Design；小修可直接调试与验证。安装状态由宿主发现，Help 同时支持查找框架内能力和相关专家。

验证分为建立配方、运行任务影响面、显式维护完整声明覆盖面。创建配方只证明已跑的代表路径；日常 Run 不宣称全量同步。结构检查、证据文件完整性、模型性质与真实产品行为分别给出结论。

Ship 由实际目标与授权决定。CI、运行或用户反馈重新进入交付流程；只有显式要求才进入 Evidence → Eval → Distill → Evolve → Doctor 的私有演化。

## 当前组成与演进

生命周期重构时，能力从 12 个调整为 14 个：增加 Decision Dialogue 与 Verification Run，删除六份重复 Playbook，将其有效方法保留到统一生命周期与 Track / Mode。随后增加 Help，目前共 15 个 Skill。日常入口收敛不改变内部能力数量。共用契约继续使用原路径，既有 Skill-only 评估快照无需额外资源注入协议。Maintain 是验证工作流的一条路径，不再增加一个 Skill。

Marketplace 现有 4 个成员：本 Harness、独立 Frontend Design、Go 专家与专业代码审查。Frontend Design 的 1 个技能属于另一个插件，正文和许可证保持固定版本；不计入 Harness 的 15 个技能。配对运行的质量、耗时、费用可观察性和安装验证见 [UI A/B 记录](frontend-design-ab.md)。

本版本没有后台任务引擎、隐式多 Agent 启动或 hooks。确定性约束由可直接运行的检查器和 CI 承担；恢复与人工协作按当前宿主能力执行。
