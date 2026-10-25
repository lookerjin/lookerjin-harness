---
name: system-understand
description: Trace an unfamiliar or cross-cutting subsystem from real entry points through state, ownership, dependencies, and observable results before explaining or changing it. Use for architecture walkthroughs, change placement, regression context, or design rationale when hidden constraints matter. Do not inventory the whole repository for a local change whose call path is already understood.
---

# System Understand

先建立足以支持当前判断的模型，再扩大阅读范围。该 Skill 产出上下文，不修改产品代码。

## 当前行为

1. 明确问题和目标入口，读取适用规则、已有项目导航及直接相关文件。已知文本用 `rg`；定义、引用和调用关系优先用可用的 LSP/符号查询，语法模式用 AST 工具；不可用时降级并保留覆盖限制。不把文本未命中当成没有调用者。
2. 沿实际调用链追踪输入转换、关键状态、所有权、外部连接、输出和失败路径。重点看接口与转换点，不逐文件讲解。
3. 核对配置、运行方式和已有验证；必要时做隔离的最小观察实验。不根据类型名或 README 独自推断运行机制。
4. 小问题直接解释。复杂问题才分成少量互不重叠的阅读角度；使用子 Agent 前遵守当前环境规则，父 Agent 复核证据并形成统一模型。

## 按需代码地图

用户要看关系、跨模块影响难以追踪、或同一区域反复探索时，按 [代码导航](references/code-navigation.md) 生成局部地图。已有明确路径的小改不建图；已有有效导航只读相关片段。地图贯穿 Design / Plan / Execute / Verify，不增加阶段或必经入口。

复用语言工具提取事实；[code-map.py](scripts/code-map.py) 只负责记录、局部查询、新鲜度检查与原生 draw.io 导出。人看的图与 Agent 的 JSON 来自同一关系集。区分 imports / calls / data-flow / state-transition / verifies，推断显式标记；模块依赖不冒充函数调用。每条关系保留源码证据，验证引用已有验收 ID。

查询前核对范围内内容指纹，包括未提交修改、新增与删除。过期图仅作历史线索，重查受影响关系后生成新快照；不自动安装工具、全库索引或后台更新。找不到解析器时仍可继续源码调查，不能编造完整图谱。

## 按需追溯决策

只有设计动机、回归历史或潜在隐藏约束影响当前判断时，查询相关文件的 `git log --follow`、`git blame`、已有设计记录及关联 PR/Issue。其他资料与 MCP 按相关性和可用性发现，不要求完整企业工具栈。

用 [execution-contract](../engineering-run/references/execution-contract.md) 的证据标签。把历史发现整理为应保留 / 可修改 / 应避免 / 未确认约束。明确说明无历史证据的动机是推断或未知，不能把“代码如此”推成“作者故意如此”。

## 交付

用最短合适形式说明入口 → 关键转换 → 状态/依赖 → 可观察结果，列出受影响边界、证据路径与未知项。只把长期有复用价值的事实写入项目已有权威位置，不默认新增架构快照或复制配置。

复用既有知识或跨会话摘要时核对其观察时间、源码版本和适用范围；历史事实不能自动代表当前实现。新证据修正原结论时记录替代关系，按 [连续性](../engineering-run/references/continuity.md) 回到项目现有事实位置。
