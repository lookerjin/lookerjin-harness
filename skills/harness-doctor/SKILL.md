---
name: harness-doctor
description: Validate the structure and internal consistency of this Agent Plugin repository. Use after changing plugin manifests, MCP configuration, skills, references, scripts, or assets in lookerjin-harness. Do not run against an adopted application repository; this script expects plugin.json and skills/ at the root.
---

# Harness Doctor

目标是验证本插件仓库是否结构正确、引用完整、可被 Agent 正确发现。它不替代项目代码测试，也不检查业务仓库。

## 使用方式

在插件仓库根目录运行：

```bash
python3.11 skills/harness-doctor/scripts/doctor.py --root . --json
```

需要 Python 3.11+（或安装 `tomli` 的 3.10）。更老的 Python 不能解析 Profile TOML，Doctor 会以错误失败，而不是 `status=pass`。

如果当前环境没有可用的 Python，则由当前 Agent 用等价方式完成同一组确定性检查，并明确标记未运行的脚本验证。

## 检查范围

- `plugin.json` 是否存在、JSON 可解析、`$schema` 与 `name` 是否合法。
- `version` 若存在则记录，缺少不当作错误。
- `mcp.json` 如果存在，是否可解析、`mcpServers` 是否为对象、各服务是否有 `type` 以及 `url` 或 `command`。
- `skills/*/SKILL.md` 必须可发现；缺 `SKILL.md` 视为错误。
- frontmatter 必须包含 `name` 和 `description`，且 `name` 与目录名一致。
- Markdown 本地链接是否指向真实路径。
- `project-bootstrap` 的 Profile TOML 是否可解析、id 是否重复。Python 无法解析 TOML 时记为错误。
- `assets/github/ci-go.yml` 是否仍保留 `REPLACE_WITH_FULL_COMMIT_SHA`。模板里丢掉占位符会导致生成仓库漏钉 SHA。
- 是否重新出现已经废弃的自定义顶层 `global/`、`profiles/`、`assets/`、`checks/`。

## 输出

默认输出适合人阅读；`--json` 输出稳定的结构化结果。

## 边界

- Doctor 只做本插件仓库的低歧义检查。
- 不扫描秘密内容，不执行项目业务测试，不替代安全审查。
- 不因为 Doctor 通过就宣称功能正确。
