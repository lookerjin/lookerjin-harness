---
name: root-cause-debug
description: Diagnose a reproducible or evidence-bearing software failure by gathering facts, forming competing hypotheses, running minimal experiments, and fixing the root cause. Use for bugs, flaky tests, crashes, race conditions, unexpected state, performance regressions, or recurring failures. Do not use for straightforward compile errors whose cause is already directly proven.
---

# Root Cause Debug

不要从第一个看起来合理的原因直接跳到修改。

## 流程

1. 定义症状、期望行为、实际行为和可观察证据。
2. 找到最小可重现路径；不能复现时，记录现有证据边界。
3. 列出少量有区分度的候选原因。
4. 为最可能或最容易排除的候选设计低成本实验。
5. 一次尽量只改变一个变量。
6. 根据实验结果淘汰或提升假设。
7. 在证据足以支持 root cause 后做最小修复。
8. 运行能证明修复真实覆盖该原因的验证。
9. 再检查是否引入新回归。
10. 汇报：
   - root cause
   - 关键证据
   - 修改
   - 已运行验证
   - 未运行/无法确认项

## 约束

- 日志、监控、测试失败、数据库状态和真实运行结果优先于模型猜测。
- 不为了“修干净”顺手处理无关历史问题。
- 对低频、难复现问题，优先保存现场证据并增加可观测性，不虚构复现结论。
