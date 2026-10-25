---
name: engineering-run
description: Carry a software engineering goal through the shortest sufficient path to a verified delivery. Use for features, fixes, refactors, investigations, prototypes, or sustained implementation. Adapt six lifecycle stages to existing facts and risk; use a narrow specialist skill directly when it already owns the task. Does not expand authorization or automatically evolve the harness.
---

# Engineering Run

以用户目标为主线，选择当前最有价值的动作。六阶段是内部状态模型，不是六项必做仪式，也不是六个 Skill。

## 用户入口

直接接收自然语言目标，结合已有对话识别“仅讨论”“给方案”“执行并验证”“继续当前任务”等范围，不要求先输入斜杠、选阶段或调用 Help。已能由窄技能完整处理的任务直接进入该技能；通用用法问题才交给 [help](../help/SKILL.md)。用户在执行中询问原因或进度时，简答后继续已授权工作，不把整个任务退回帮助流程。

按当前宿主实际能力加载技能：有技能调用能力就使用；只有安装文件可读时直接读取对应 `SKILL.md` 及必要引用，按其说明执行。具体命令语法以宿主实际提供的为准，不依赖专属 alias、菜单隐藏或固定工具名称。资源存在、技能被发现和外部工具可用是三个独立事实。

## 建立任务契约

读取适用项目规则与直接相关事实，沿用用户已有修改和授权。用一句目标加必要的范围、验收、验证入口、交付目标建立 [执行契约](references/execution-contract.md)。简单任务在当前会话表达即可；复杂任务复用项目计划，避免另外建立一份事实库。

把四个维度分开：

| 维度 | 选择 |
|---|---|
| Lifecycle：当前需要解决什么阶段问题 | Brainstorm / Design / Plan / Execute / Verify / Ship |
| Track：目标是什么 | Feature / Bug Fix / Refactor / Investigate |
| Mode：怎么推进 | 默认直接执行；按需组合 Prototype / Long Run / Parallel / Subagent |
| Capability：需要谁或什么 | 现有领域 Skill、专家能力、Human、MCP、工具 |

按 [生命周期](references/lifecycle.md) 选择入口、跳过已满足的阶段并允许回退；按 [任务与执行方式](references/tracks-and-modes.md) 选择一个主 Track 和必要 Mode。只加载当前问题所需资源，不逐项调用整个目录。

涉及页面、组件、视觉或交互时，按需使用 [UI 能力接入](references/ui-capabilities.md)，将设计、实现和真实界面验证交给适用能力；UI 沿用当前生命周期，不增加必经阶段或默认安装。

## 推进与切换

1. 先识别决定下一动作的不确定性：仓库可回答的自己查；用户掌握的关键决定交给 [decision-dialogue](../decision-dialogue/SKILL.md)。真人观察、操作或判断更有效时按 [协作契约](references/collaboration.md) 请求最小帮助，继续不依赖回答的工作。
2. 已有充分事实的小改直接 Execute → Verify。实质结构选择使用 Design Explore；需要理解已有关系用 System Understand；缺陷机制交给 Root Cause Debug；依赖选型交给 Dependency Evaluation。工程规则缺失才用 Project Bootstrap / Adopt。
3. 大任务拆成可独立验收的 Unit，先走通一条纵向切片再扩展。按依赖取就绪项，未验证的前置不能当作完成；可选用 [check-plan.py](scripts/check-plan.py) 检查依赖与记录结构。它不替代任务判断，也不要求小任务写 JSON。
4. Execute 与 [verification-run](../verification-run/SKILL.md) 交替。没有可用配方才用 Verification Bootstrap；验证指出实现错误回 Execute，假设错误回 Design，目标冲突回 Brainstorm。重跑受影响范围，不清空已证实的无关结果。
5. 用 Change Review 检查实际 diff、质量底线、证据适用性和未覆盖风险。修复后补验受影响项。按 [连续性](references/continuity.md) 保存可恢复状态。
6. Ship 达成用户实际要求的交付状态：可交接 / commit / push / PR / deploy / release；只执行已经授权的部分。有关键缺口则明确部分交付。现实反馈作为新任务进入合适阶段，先判断现象和影响范围。

交付完成不自动调用 Harness Evolve。只有用户明确要求改进自身方法时才进入私有演化流程。
