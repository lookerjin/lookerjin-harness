---
name: harness-eval
description: Evaluate whether a skill or harness revision changes agent behavior on realistic tasks using identical project snapshots, isolated outputs, a fixed rubric, and version-blind judgment. Use before promoting a workflow change or when instructions look better but their practical benefit is unknown. Structure checks and script tests do not count as behavioral evaluation; do not claim improvement from a single self-review.
---

# Harness Eval

评估任务结果、证据和副作用，不评价 Prompt 看起来是否专业。完整流程与报告字段见 [protocol](references/protocol.md)；按需从 [cases](references/cases.md) 选择有区分度的场景。

## 准备

1. 固定旧版、新版、项目起始状态与自然用户请求。在控制区先写 3～6 个可观察标准与关键否决条件，之后不因结果不喜欢而改评分。
2. 选相同模型/预算/工具/环境；要比较模型时单独做实验，避免把模型差异当 Skill 收益。
3. 使用小型、无敏感资料的已提交 Git 项目准备隔离副本。脚本只读输入，不安装到用户客户端、不启动 Agent、不联网、不提交、不推送：

```bash
python scripts/prepare.py --project <fixture-repo> --ref HEAD \
  --baseline-skills <old-skills-dir> --candidate-skills <new-skills-dir> \
  --output <new-output-dir> --seed 0
```

在本 Skill 目录运行；否则使用脚本安装后的真实路径。目录参数是本次实际路径，不能原样执行占位值。`--skills-path` 默认 `skills`，碰到项目已有目录时选一个不冲突的相对路径。输出的 `projects/cedar` 与 `projects/birch` 是独立副本；版本映射和内容指纹在 `control/assignment.json`，不传给执行者或判断者。

Git 副本检出指定 commit，保留项目历史，使用独立对象存储并移除 origin；不共享工作区、不创建新 commit。注入的 Skill 在副本的 `.git/info/exclude` 中排除，项目修改仍能正常查看 diff。历史本身也须为可提供给执行者的脱敏资料。外部依赖、未跟踪数据与 submodule 不包含在内；需要时由控制者按同一配方补足，或者改用现有隔离环境，无法匹配就标不确定。脚本拒绝符号链接与已有输出目录，不覆盖用户文件。

## 运行与判断

按 Protocol 启动可用的独立会话/子 Agent，只提供各自工作目录、需要的 Skill 位置和相同自然任务，不告诉它旧/新版、评分、预期修复或其他候选。依当前环境规则使用能力，不能因本 Skill 自动取得启动或外部操作授权。

执行者结束后冻结产物，把相同标准与按中性标签提供的原始产物交给独立判断者；版本映射仍留在控制区。父 Agent 必须读产物并核对实际运行和副作用。没有独立能力时可以做串行受限试验，但上下文泄漏和独立性不足须写入限制；不能当成干净盲评。

## 收敛

逐案例报告结果、证据、关键失败和覆盖缺口，建议保留候选 / 修改后重试 / 拒绝 / 无法判断。任何关键项不确定都不计为通过。结构正确、脚本可运行与真实行为有效分别汇报；少量案例只支持这些场景的判断，不证明跨项目长期收益。
