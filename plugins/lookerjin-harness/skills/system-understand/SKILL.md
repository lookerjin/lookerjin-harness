---
name: system-understand
description: Trace an unfamiliar or cross-cutting subsystem from real entry points through state, ownership, dependencies, and observable results before explaining or changing it. Use for architecture walkthroughs, change placement, regression context, or design rationale when hidden constraints matter. Do not inventory the whole repository for a local change whose call path is already understood.
---

# System Understand

先建立足以支持当前判断的模型，再扩大阅读范围。该 Skill 产出上下文，不修改产品代码。

## 当前行为

1. 明确问题和目标入口，读取适用规则及直接相关文件。优先 `rg` 找入口、符号和调用者。
2. 沿实际调用链追踪输入转换、关键状态、所有权、外部连接、输出和失败路径。重点看接口与转换点，不逐文件讲解。
3. 核对配置、运行方式和已有验证；必要时做隔离的最小观察实验。不根据类型名或 README 独自推断运行机制。
4. 小问题直接解释。复杂问题才分成少量互不重叠的阅读角度；使用子 Agent 前遵守当前环境规则，父 Agent 复核证据并形成统一模型。

## 按需追溯决策

只有设计动机、回归历史或潜在隐藏约束影响当前判断时，查询相关文件的 `git log --follow`、`git blame`、已有设计记录及关联 PR/Issue。其他资料与 MCP 按相关性和可用性发现，不要求完整企业工具栈。

用 [execution-contract](../engineering-run/references/execution-contract.md) 的证据标签。把历史发现整理为应保留 / 可修改 / 应避免 / 未确认约束。明确说明无历史证据的动机是推断或未知，不能把“代码如此”推成“作者故意如此”。

## 交付

用最短合适形式说明入口 → 关键转换 → 状态/依赖 → 可观察结果，列出受影响边界、证据路径与未知项。只把长期有复用价值的事实写入项目已有权威位置，不默认新增架构快照或复制配置。
