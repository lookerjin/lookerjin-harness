---
name: design-explore
description: Explore structurally different designs before implementing a consequential interface, ownership, state, or module decision. Use for architecture forks, contested designs, repeated implementation friction, or a cheap prototype that can settle a costly assumption. Do not require multiple candidates for routine local edits or decisions already fixed by project constraints.
---

# Design Explore

以调用者的使用方式和真实约束组织方案比较，不凭完整漂亮的方案文档决定。

1. 用 [system-understand](../system-understand/SKILL.md) 建立必要上下文。列出验收行为、必须保留的契约和还不确定的关键变量。
2. 先写 3～6 项与当前问题有关的比较标准，例如调用复杂度、状态所有权、错误恢复、外部兼容性、维护与迁移成本。
3. 生成 2～3 个结构不同的候选，包含最小可行方案。每个给出调用者用法、数据/接口草图、状态与失败路径、取舍和证伪方式；命名变化不算新候选。
4. 优先通过低成本、可逆实验验证决定性假设。顺序推演、独立子 Agent 或多模型都可用，但只在当前环境允许时启动；不硬编码模型或要求 fan-out。顺序产生的候选注明不是独立采样。
5. 对同一标准比较所有候选。独立判断者只看需求、约束与候选原始产物，不看父 Agent 的偏好；不可用时做直接比较并说明限制。最终由负责人判断，不按票数决定。
6. 收敛为一个一致方案，说明采用和拒绝的理由，以及尚未验证的假设。不同方案会明显改变长期方向且资料不能决定时，向用户提出具体选择；本地可逆决定可继续实现。
7. 实现中出现重复同类绕路、所有权泄露或接口需要频繁逃逸时，回到事实与候选比较。单个边界条件不足以证明架构错误；不要无限重设计或顺手重写无关部分。

交付所选方案、关键取舍、实验结果与可检查的验收。方案草图不是功能验证，最终组合仍需真实行为验证。
