# 自适应执行核心

Engineering Run 将目标、验收与已有授权映射为最短充分路径。六阶段允许跳过、回退和局部交付；领域能力按需调用，专业能力通过当前客户端接入。

- [架构与具体文件职责](architecture-refactor.md)
- [架构图：原生 draw.io](architecture-refactor.drawio)
- [用户旅程：原生 draw.io](user-journey.drawio)
- [本项目运行记录](field-tests.md)

## 运行边界

共同执行契约属于 `engineering-run/references`，调用它只加载资源，不额外调用一个“契约 Skill”。Track 不各自维护一套阶段，Mode 不取代目标。人提供决定或观察时 Agent 继续独立工作。

验证分为建立配方、运行任务影响面、显式维护完整声明覆盖面。创建配方只证明已跑的代表路径；日常 Run 不宣称全量同步。结构检查、证据文件完整性、模型性质与真实产品行为分别给出结论。

Ship 由实际目标与授权决定。CI、运行或用户反馈重新进入交付流程；只有显式要求才进入 Evidence → Eval → Distill → Evolve → Doctor 的私有演化。

## 本次结构变更

能力从 12 个收敛为 14 个：增加 Decision Dialogue 与 Verification Run，删除六份重复 Playbook，将其有效方法保留到统一生命周期与 Track / Mode。共用契约继续使用原路径，既有 Skill-only 评估快照无需额外资源注入协议。Maintain 是验证工作流的一条路径，不再增加一个 Skill。

本版本没有后台任务引擎、隐式多 Agent 启动或默认 hooks。确定性约束由可直接运行的检查器和 CI 承担；恢复与人工协作按当前宿主能力执行。
