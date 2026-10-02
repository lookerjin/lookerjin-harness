# 轻量工程执行层

本次扩展保持现有 Plugin、Marketplace 和 Expert Plugin 边界。新增的执行逻辑使用普通 Skill 和按需 references，不引入独立 runtime、Hook、顶层协议或插件间依赖。

## 权威位置

| 内容 | 位置 |
|---|---|
| 意图路由与能力组合 | [engineering-run](../skills/engineering-run/SKILL.md) |
| 各类任务阶段 | engineering-run/references/playbooks/ |
| 共同授权、证据与验证语义 | [execution-contract](../skills/engineering-run/references/execution-contract.md) |
| 具体项目怎么运行与验证 | 项目现有 scripts / CI / 验证配方 |
| 自动经验晋升门槛 | [promotion-policy](../skills/harness-evolve/references/promotion-policy.md) |
| 行为比较方法 | [harness-eval](../skills/harness-eval/SKILL.md) |
| 实际实验结果 | [field-tests](field-tests.md) |

AGENTS 继续约束插件维护，Project Bootstrap 的 engineering-defaults 继续提供目标项目规则素材；不把执行契约复制成另一份全局原则。

## 参考源码

先在云端拉取 `cursor/plugins`，固定到 `fae2c6ed95821bd85f614a73e4842e13229fa5e5`，阅读本地 `pstack` 0.15.5。下表链接均固定该版本。本次按已有 Harness 边界重新编写中文流程，没有复制其 Cursor manifest、agents 或执行 runtime。

| 一手文件 | 吸收内容 | 本实现取舍 |
|---|---|---|
| [poteto-mode](https://github.com/cursor/plugins/blob/fae2c6ed95821bd85f614a73e4842e13229fa5e5/pstack/skills/poteto-mode/SKILL.md) | 意图路由与 Playbook | 仅六类任务，不加载整套原则目录，不自动 PR |
| [bug-fix](https://github.com/cursor/plugins/blob/fae2c6ed95821bd85f614a73e4842e13229fa5e5/pstack/skills/poteto-mode/playbooks/bug-fix.md) | 机制证据与同入口复跑 | 合并进 Root Cause Debug；保留用户 Git 授权边界 |
| [how](https://github.com/cursor/plugins/blob/fae2c6ed95821bd85f614a73e4842e13229fa5e5/pstack/skills/how/SKILL.md) / [why](https://github.com/cursor/plugins/blob/fae2c6ed95821bd85f614a73e4842e13229fa5e5/pstack/skills/why/SKILL.md) | 行为模型与历史约束 | 合成按需 System Understand，不默认七类企业调查 |
| [architect](https://github.com/cursor/plugins/blob/fae2c6ed95821bd85f614a73e4842e13229fa5e5/pstack/skills/architect/SKILL.md) / [arena](https://github.com/cursor/plugins/blob/fae2c6ed95821bd85f614a73e4842e13229fa5e5/pstack/skills/arena/SKILL.md) | 不同结构候选、共同标准、综合与重新设计 | Design Explore，不写死模型，不强制并行 |
| [create-verification-skill](https://github.com/cursor/plugins/blob/fae2c6ed95821bd85f614a73e4842e13229fa5e5/pstack/skills/create-verification-skill/SKILL.md) | 从项目发现 launch/drive/observe/cleanup 并跑通 | 使用项目已有位置和脚本，不默认 Cursor 目录或大量 feature map |
| [interrogate](https://github.com/cursor/plugins/blob/fae2c6ed95821bd85f614a73e4842e13229fa5e5/pstack/skills/interrogate/SKILL.md) | 独立 finding、分歧图与负责人判断 | 加强 Change Review，不新建同义 Skill |
| [eval](https://github.com/cursor/plugins/blob/fae2c6ed95821bd85f614a73e4842e13229fa5e5/pstack/skills/poteto-mode/playbooks/eval.md) | 同任务、版本盲判与原始产物 | 不强制多模型，不删除正常项目测试，不将共享文件系统称为安全隔离 |
| [reflect](https://github.com/cursor/plugins/blob/fae2c6ed95821bd85f614a73e4842e13229fa5e5/pstack/skills/reflect/SKILL.md) | 会话原始证据采集 | 合并进 Evolve，仍需重复发生与归属判断 |
| [orchestrate](https://github.com/cursor/plugins/blob/fae2c6ed95821bd85f614a73e4842e13229fa5e5/pstack/skills/poteto-mode/playbooks/orchestrate.md) | Unit 契约、先跑 pilot | 轻量 Long Run，不实现 ledger/queue/多日调度 |

上游 `pstack/LICENSE` 为 MIT，作者 Lauren Tan。此处记录设计来源；未来直接引入上游实现或大段原文时需要保留其相应版权与许可证。

## 当前边界

这是明确要求的候选改造，不是已经完成跨项目长期晋升。结构和脚本验证、独立夹具行为与真实项目 field test 分别记录。下一步优先在一个真实 bug、一个功能和一个长任务中运行，观察误触发、漏验证与执行成本，再决定调整或删减。
