# Open Code Review 适配

这是 Change Review 使用独立专业审查能力的组合约定，不是新的插件协议。上游入口、版本选择与安装策略以 Marketplace 清单为准；OCR CLI 与插件包分别安装、分别更新。CLI 命令和 JSON 字段以实际版本为准，不复制上游规则库或维护第二份审查引擎。

## 职责

| 归属 | 职责 |
|---|---|
| Harness / Change Review | 固定范围、核对覆盖与业务契约、检查运行证据、判断 findings、决定交付状态 |
| OCR / 专业审查 | 文件选择、语言规则与缺陷 findings；完整模式另有其审查执行、定位与后处理 |
| 项目 | 项目规则、实际启动/操作/观察/清理配方、测试与 CI |
| 主 Agent | 读取对应 Skill、调用可用工具、补齐遗漏、在授权范围内修复并复验 |

## 模式与可用性

- 默认优先委托模式 `open-code-review-delegate`：OCR 负责确定性的文件选择与规则解析，宿主 Agent 负责推理；不配置额外 OCR 模型 Key。它不等于独立审查者，也不自动获得完整模式的定位/反思流程。
- 用户指定完整模式，或已明确选择使用配置好的 OCR 外部模型时，使用上游 `open-code-review` Skill；在运行前核对代码传输范围、模型和本次预算。委托模式的选择不授权调用外部模型。
- 需要当前客户端能运行 `ocr` 和 Git；市场条目可发现不等于客户端已经安装、CLI 已存在或模式已跑通。初始验证使用 CLI v1.12.11；升级后重新检查实际命令、schema、规则和过滤行为。
- 不为一般变更验收强制安装、全局升级 CLI 或索取 API Key。能力不可用时报告原因并执行可用的领域审查；用户明确要求 OCR 时，不把降级审查冒充 OCR 成功。

## 范围、敏感文件与规则

1. 与 Change Review 使用同一工作区、commit 或 base/head。分支模式确认 merge-base；源码变化后报告不能覆盖新版本。
2. 内容读取或外部模型调用前，对完整目标文件清单应用项目排除策略和预检脚本 `SENSITIVE_BASENAME_PATTERNS` 的敏感文件名检查。当前预检只对未跟踪内容自动跳过；已跟踪文件也要检查路径，不能因为已提交就默认可发送。把确认的排除模式显式传给 OCR，并核对 preview 的实际结果；无法保证排除时跳过受影响的 OCR 路径。
3. OCR 内置秘密路径过滤只覆盖其已定义模式，不能替代项目策略。CLI 的 `--exclude` 与规则文件可能有不同匹配语义，以实际 preview 为准；不要把凭证内容放进 background、临时规则或报告。
4. 对照全量变更与 `reviewable_files`、`excluded_files`：每个文件记录已审查 / 有理由排除 / 尚未审查。测试、Markdown、配置和其他 OCR 未覆盖内容，按变更影响由主 Agent 补查。专家的 coverage 分母不能直接充当全量变更的验收分母。
5. 项目明确规则优先。业务背景传入目标、约束和验收，不把已加载的 AGENTS 或专家知识假定为外部模型自动拥有。复用现有 `.opencodereview/rule.json`；只有确有缺口才补配置。
6. OCR 自定义规则默认替换匹配的内置规则；需要共同使用时显式设置 `merge_system_rule: true`，运行 rule 查询确认。不要复制整份语言规则，也不另建项目规则的权威来源。

## 委托模式调用

下面是命令形状，尖括号参数替换为本次实际值并用当前 shell 安全传参。排除模式需包含本次已确认的敏感/项目排除项，不把不可信文本直接拼进 shell。

```bash
ocr delegate preview --format json --repo <repo> --exclude <patterns>
ocr delegate preview --format json --repo <repo> --from <base> --to <head> --exclude <patterns>
ocr delegate preview --format json --repo <repo> --commit <commit> --exclude <patterns>
ocr delegate rule --format json --repo <repo> <reviewable-paths>
```

按需为两类命令都传同一 `--rule <existing-rule-file>`，确认最终规则和覆盖范围一致。只读取对应目标的 diff 和必要调用上下文，逐批按规则审查。上游 Skill 的 reviewed/skipped 清单需要核对实际文件和范围，不能只填覆盖率。

## 输出与验收

- 保留模式、CLI 版本、目标 refs/源码状态、实际命令、退出码、必要原始输出、选中/排除/已审查/失败文件与原因。
- 完整模式用文件保存 JSON 结果并读完，核对 warnings、failed/skipped、预算状态和实际覆盖。退出码 0 或零 findings 不代表全量审查完成，更不等于项目行为已验证。
- 对 findings 逐项确认可达路径和证据，合并重复项；项目风格建议与真实缺陷分开。记录处理 / 待权衡 / 记录 / 驳回及理由，负责人判断不按专家数量投票。
- 只在原任务已授权修复时修改产品；修复后执行受影响项目验证，并更新对应范围的审查结果。无论采用哪种 OCR 模式，运行证据和最终状态仍使用 [execution-contract](../../engineering-run/references/execution-contract.md)。
- 不自动提交、推送、创建 PR 或发布外部审查评论。完整模式未运行、过滤内容未补查、或证据不足时明确保留相应缺口。
