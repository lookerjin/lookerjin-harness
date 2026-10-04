---
name: root-cause-debug
description: Diagnose a reproducible or evidence-bearing software failure by gathering facts, forming competing hypotheses, running minimal experiments, and fixing the root cause. Use for bugs, flaky tests, crashes, race conditions, unexpected state, performance regressions, or recurring failures. Do not use for straightforward compile errors whose cause is already directly proven.
---

# Root Cause Debug

不要从第一个看起来合理的原因直接跳到修改。

## 流程

1. 定义症状、期望行为、实际行为和可观察证据。
2. 从用户实际入口找到最小可重现路径，记录输入、配置、前提、失败表现和观察点；不能复现时，记录现有证据边界。
3. 必要时用 [system-understand](../system-understand/SKILL.md) 追踪受影响调用链与回归历史；列出少量有区分度的候选原因。
4. 选择能排除最多关键候选的低成本实验。能二分就二分，不强迫不适用的问题使用二分。
5. 一次尽量只改变一个变量。
6. 根据实验结果淘汰或提升假设。
7. 用运行证据说明触发条件如何通过具体机制导致症状；源码可直接证明的确定性错误可以使用直接证据。只在证据足以支持 root cause 后做最小修复；被证伪假设引入的临时修改要撤回。
8. 修复后从同一入口、可比配置与输入复跑原始触发路径；验证配方缺失时使用 [verification-bootstrap](../verification-bootstrap/SKILL.md)。在项目允许的证据位置保留修复前失败与修复后结果，包含本次实际命令、退出码及必要原始输出（CLI 的 stdout/stderr、UI 的动作与状态等），不要只写“已通过”的总结。廉价且有回归价值时补能先失败后通过的行为用例；不为此擅自提交。
9. 再检查是否引入新回归。
10. 汇报：
   - root cause
   - 关键证据
   - 修改
   - 已运行验证
   - 未运行/无法确认项

## 约束

- 用 [execution-contract](../engineering-run/references/execution-contract.md) 记录 `VERIFIED` / `NOT_VERIFIED` / `INCONCLUSIVE`。单测通过但原始入口无法复跑时，不声明原 bug 已验证修复。
- 日志、监控、测试失败、数据库状态和真实运行结果优先于模型猜测。
- 不为了“修干净”顺手处理无关历史问题。
- 对低频、难复现问题，优先保存现场证据并增加可观测性，不虚构复现结论。
