---
name: decision-dialogue
description: Resolve consequential unknowns in a software goal or design through dependency-aware questions with recommendations. Use when user knowledge or preferences determine scope, acceptance, interfaces, or architecture, or when the user asks to be grilled. Inspect accessible facts yourself. Do not turn an explicit small implementation request into a mandatory interview.
---

# Decision Dialogue

先明确本次要解决的决定范围。阶段中的局部澄清只处理阻塞当前选择的部分；用户明确要求完整追问时才系统覆盖整个提案。

1. 读取已有目标、约束、相关代码与用户已经给出的答案。把可自行验证的事实先查清，不把调查工作转给用户。
2. 按 [依赖前沿](references/frontier.md) 列待决问题及依赖；给当前已就绪问题提供推荐、真实备选及后果。未决前提会改变问题含义时暂不问下游问题。
3. 用当前客户端问答能力询问，遵守工具单次容量。可分批呈现当前前沿，但不设任意总问题数或轮数，也不一次抛出未来所有问题。
4. 等待必需答案，继续不依赖回答的工作。收到回答后确认含义，更新决定与下游问题，删除失效候选，再计算前沿。
5. 局部澄清在当前阻塞解除时返回原阶段；完整追问在当前范围关键前沿清空、共同理解得到用户确认后结束。用户决定停止时交付已知决定和剩余未知，不虚称完整。

输出：已决定事项及理由、明确不做什么、验收影响、仍未解决项、下一动作。通常在会话或已有计划保留；只有长期结构取舍需要 ADR，只有术语歧义影响实现时才维护领域词汇。
