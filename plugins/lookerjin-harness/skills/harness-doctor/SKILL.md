---
name: harness-doctor
description: Validate the structure and internal consistency of this Codex plugin. Use after changing the Codex manifest, MCP configuration, skills, references, scripts, or assets in lookerjin-harness. Do not run against an adopted application repository; this script expects .codex-plugin/plugin.json and skills/ at the plugin root.
---

# Harness Doctor

目标是验证本插件是否结构正确、引用完整、可被 Codex 正确发现。它不替代项目代码测试，也不检查业务仓库。

## 使用方式

在插件根目录运行：

```bash
python3.11 skills/harness-doctor/scripts/doctor.py --root . --json
```

运行时契约：Python 3.11+，仅使用标准库。Doctor 依赖标准库 `tomllib` 解析 Profile TOML，不提供 Python 3.10 + 第三方兼容层。

如果当前环境没有 Python 3.11+，由当前 Agent 用等价方式完成同一组确定性检查，并明确标记 Doctor 脚本未运行。

## 检查范围

- `.codex-plugin/plugin.json` 是否存在、JSON 可解析、`name` 与 `version` 是否合法。
- 根目录不应再保留第二份 `plugin.json`，避免双 manifest 漂移。
- Manifest 中声明的 `skills`、`mcpServers`、`logo`、`logoDark`、`composerIcon` 和 screenshots 是否使用安全的插件相对路径并真实存在。
- `mcp.json` 如果存在，是否可解析、`mcpServers` 是否为对象、各服务是否有 `type` 以及 `url` 或 `command`。
- `skills/*/SKILL.md` 必须可发现；缺 `SKILL.md` 视为错误。
- frontmatter 必须包含 `name` 和 `description`，且 `name` 与目录名一致。
- Markdown 本地链接是否指向真实路径。
- `project-bootstrap` 的 Profile TOML 是否可解析、id 是否重复。
- `skills/project-bootstrap/assets/github/ci-go.yml` 是否仍保留 `REPLACE_WITH_FULL_COMMIT_SHA`。
- 是否重新出现已经废弃的自定义顶层 `global/`、`profiles/`、`checks/`。

根级 `assets/` 是合法的插件资源目录，不应被视为 legacy layout。

## 输出

默认输出适合人阅读；`--json` 输出稳定的结构化结果。

## 边界

- Doctor 只做本插件的低歧义结构检查。
- 不扫描秘密内容，不执行项目业务测试，不替代安全审查。
- 不因为 Doctor 通过就宣称功能正确。
