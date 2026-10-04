# Feature

状态：Ground → Design → Implement → Verify → Review。

1. 用 [system-understand](../../../system-understand/SKILL.md) 追踪受影响入口、接口、状态与已有验证。新项目先用 Project Bootstrap，仅初始化本次需要的部分。
2. 定义验收行为与数据、接口、所有权边界。存在实质结构选择时用 [design-explore](../../../design-explore/SKILL.md)；直观小改动直接选最小方案。新增依赖时用 Dependency Evaluation。
3. 按可验证步骤实现，只改当前范围。相互依赖的修改由一个负责人推进；独立修改才考虑并行。
4. 复用项目已有验证入口。缺少操作配方时用 [verification-bootstrap](../../../verification-bootstrap/SKILL.md)。观察真实路径的输入、结果与副作用，修复失败并重新执行。
5. 用 [change-review](../../../change-review/SKILL.md) 检查实际 diff、回归和文档影响。

退出门槛：关键验收已验证，评审发现已处理。存在外部阻塞时报告部分完成及缺口；不能用构建成功替代行为验收。
