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
8. 明确区分：已验证 / 部分验证 / 未运行 / 无法确认。
9. 输出 findings 优先；没有问题时明确说明证据范围。

## 禁止

- 不自动 commit、push 或创建 PR。
- 不把无关历史问题混入本次修改。
