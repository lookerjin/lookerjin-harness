---
name: harness-doctor
description: Validate the structure and internal consistency of this Agent Plugin or an adopted project harness. Use after changing plugin manifests, MCP configuration, skills, references, scripts, assets, or generated project harness files. Prefer deterministic checks and machine-readable output; do not perform unrelated code review.
---

# Harness Doctor

目标是验证 Harness 是否结构正确、引用完整、可被 Agent 正确发现，而不是替代代码测试或架构评审。

## 使用方式

在插件仓库根目录运行：

```bash
python skills/harness-doctor/scripts/doctor.py --root . --json
```

如果当前环境没有 Python 3，则由当前 Agent 用等价方式完成同一组确定性检查，并明确标记未运行的脚本验证。

## 检查范围

- `plugin.json` 是否存在、JSON 可解析、schema 与必要字段是否合理。
- `mcp.json` 如果存在，是否可解析且 `mcpServers` 为对象。
- `skills/*/SKILL.md` 是否可发现，frontmatter 是否包含 `name` 和 `description`。
- Skill frontmatter 的 `name` 是否与目录名一致、是否重复。
- Markdown 本地链接是否指向真实路径。
- `project-bootstrap` 的 Profile TOML 是否可解析、id 是否重复。
- 是否重新出现已经废弃的自定义顶层 `global/`、`profiles/`、`assets/`、`checks/`。

## 输出

默认输出适合人阅读；`--json` 输出稳定的结构化结果：

```json
{
  "status": "pass",
  "errors": [],
  "warnings": [],
  "checks": []
}
```

每个问题应有稳定 `code` 和明确 `message`，方便 Agent 自动定位和修复。

## 边界

- Doctor 只做低歧义、确定性检查。
- 不扫描秘密内容，不执行项目业务测试，不替代安全审查。
- 不因为 Doctor 通过就宣称功能正确。
- 如果某项验证依赖当前环境缺失的运行时或工具，报告为 warning / unverified，而不是猜测通过。
