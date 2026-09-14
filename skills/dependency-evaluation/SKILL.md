---
name: dependency-evaluation
description: Evaluate whether to add, replace, or avoid a third-party software dependency. Use when a task proposes a new library/framework/SDK, when custom infrastructure code may be replaceable by a mature package, or when an existing dependency becomes risky. Do not trigger for ordinary use of dependencies already accepted by the project.
---

# Dependency Evaluation

目标不是“尽量不加依赖”，而是降低系统总复杂度并保留清晰替换边界。

## 顺序

1. 标准库或平台原生能力能否清晰解决？
2. 项目已有依赖是否已提供？
3. 问题属于项目核心领域语义，还是通用基础设施？
4. 对通用基础设施，搜索当前成熟实现。
5. 核对：
   - 官方仓库与维护状态
   - 当前稳定版本
   - License
   - 语言/运行时最低版本
   - 传递依赖
   - CGO / native / platform 要求
   - 供应链和安全风险
   - API 稳定性与替换成本
6. 涉及外部库当前 API 时优先使用 Context7 或官方文档，不凭模型记忆。
7. 对关键依赖做最小 PoC 或局部真实运行。
8. 比较“自研成本 + 长期维护”与“引入依赖成本 + 锁定风险”。
9. 给出 adopt / defer / reject，并明确证据与边界。

## 触发提醒

- 准备自己实现明显属于成熟基础设施、且预计会快速膨胀的代码时，应主动评估依赖。
- 为很小的局部逻辑引入大型框架时，也应重新评估。
