---
name: change-review
description: Review a completed local code change before commit, push, or PR by inspecting the actual diff, affected behavior, verification evidence, documentation impact, and unrelated modifications. Use after implementation or before externalizing changes. This skill is review-first and does not authorize commit, push, or PR creation.
---

# Change Review

以真实 diff 和运行证据为准，不根据“模型认为已经完成”判断。

## 1. 先收集工作区事实

在目标仓库运行：

```bash
python skills/change-review/scripts/preflight.py --root . --json
```

如果当前使用环境不是本插件仓库，改用这个 Skill 安装后的本地脚本路径。脚本负责 status、diffstat、staged diff、未跟踪文件列表，以及 `untracked_diff`（把普通未跟踪文本文件当成相对 `/dev/null` 的 diff）。空的 `diff_stat` 不代表没有改动。模型不要用猜测替代这份输出，也不要为了制造 diff 而 `git add`。

高概率敏感文件名（例如 `.env*`、私钥、credentials/secrets 文件）只报告路径和大小，不展开内容；binary 或过大的文件也只报告元数据。这是安全边界，不应为了“完整 diff”绕过。

没有 Python 时，用等价 git 命令收集同一组字段，并标记脚本未运行。

## 2. 审查

1. 区分用户已有修改、Agent 修改和未跟踪文件。
2. 检查实际 diff，包括可安全展开的 `untracked_diff`，而不是只看改过的文件名。
3. 识别行为变化、接口变化、数据/状态变化和潜在兼容性影响。
4. 检查错误路径、边界条件和副作用。
5. 检查测试是否覆盖真实行为，而不是镜像实现。
6. 检查应该同步的 docs / config / migration / examples。
7. 使用项目既有快速/完整门禁，验证范围与改动相称。
8. 按 [execution-contract](../engineering-run/references/execution-contract.md) 区分 `VERIFIED` / `NOT_VERIFIED` / `INCONCLUSIVE`，说明入口、证据与未覆盖边界；整体存在缺口时报告部分验证。
9. 输出 findings 优先；没有问题时明确说明证据范围。

## 3. 按需独立审查

普通修改由当前 Agent 直接审查。复杂、高风险或有争议的变更，可在当前环境允许时使用独立审查；没有子 Agent 或多模型时做顺序审查并说明独立性限制。

- 固定同一 diff/源码状态，提供目标、约束、必要上下文与验收证据，不传父 Agent 的预期结论。审查者只读，不自行应用修改。
- 按当前风险选少量有信息增量的视角，或用同一标准独立审查。合并相同 finding，记录一致与分歧。
- 父 Agent 逐项核对真实触发路径和证据，归为处理 / 待权衡 / 记录 / 驳回，并写原因；多人同意只是信号，单人发现的真实问题也要处理。
- 修改后重跑受影响验证，审查结论绑定最终 diff；审查旧版本不能覆盖后来的改动。

## 禁止

- 不自动 commit、push 或创建 PR。
- 不把无关历史问题混入本次修改。
