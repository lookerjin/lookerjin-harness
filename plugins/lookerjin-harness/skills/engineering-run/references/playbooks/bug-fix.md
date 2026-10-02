# Bug Fix

状态：Repro → Hypothesis → Experiment → Mechanism → Fix → Same-surface Verify → Review。

按 [root-cause-debug](../../../root-cause-debug/SKILL.md) 执行完整排查。该 Skill 拥有复现、竞争性假设、实验与根因证据要求，不在这里复制。

涉及现有系统关系时先读 System Understand；跨模块修复存在实质方案选择时读 Design Explore。验证操作配方缺失时使用 Verification Bootstrap。

保持原始失败记录；修复后从同一入口复跑触发路径，检查相关回归，再用 Change Review 检查 diff。失败先于修复的顺序由证据记录或廉价回归用例证明；是否形成 commit 由已有授权决定。

退出门槛：失效机制有证据，原始触发行为在可比条件下已验证修复。难以复现时保存现场、补观察点并报告不确定性；不要把猜测修补称为已证明根因。
