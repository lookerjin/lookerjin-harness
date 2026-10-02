---
name: verification-bootstrap
description: Establish or repair a project-local recipe for verifying the actual UI, CLI, API, mobile, desktop, or library caller behavior. Use when an adopted project lacks concrete launch/drive/observe/cleanup instructions, when existing verification cannot reach a changed surface, or when asked to create a verify-app skill. Reuse existing checks and conventions; do not redesign product code or treat harness-doctor as application verification.
---

# Verification Bootstrap

Harness 定义证据标准，项目定义怎么证明。先读仓库，复用现有配方；没有复用价值的一次性检查直接运行，不强制创建 Skill。

## 发现

从入口代码、README、Makefile/scripts、测试和 CI 确认：

- **Surface**：用户或调用者实际入口，多个入口注明本次覆盖范围。
- **Launch**：真实命令、运行目录、构建与环境前提、就绪信号。
- **Drive**：已有 browser、PTY、HTTP、CLI、公开 library API 或平台测试入口。
- **Observe**：输入动作、输出内容、错误与持久化/消息等副作用。
- **Isolate / Cleanup**：本次实例、端口、数据目录与进程所有权，失败时怎么回收，证据保存在哪。

识别“有单测但没有真实入口配方”的缺口。缺少认证、平台或必要外部资源时明确阻塞，不虚构命令、选择器或 mock 验证结论。

## 建立配方

1. 已有有效项目验证时保留其权威位置，只补当前缺口。否则使用 [recipe-shape](references/recipe-shape.md)，把具体配方放到项目已有 Skill/验证文档位置；发现目录的约定由当前客户端决定，不把 `.cursor/` 等写成可移植默认。
2. 若需要 `verify-<app>`，使用 name/description frontmatter，指向已有 scripts、配置与文档。不复制同一套启动事实。只列当前真实可发现的关键路径，不预建大量 feature 文件。
3. 写入前说明路径和原因；会覆盖不可恢复内容或涉及外部操作时按已有规则确认。新增 helper 时给出明确调用方式并实际运行。
4. 启动失败先判断是否配方问题；修配方在范围内，修产品实现需交回原任务或报告。不要扩大成环境重建项目。

## 证明与维护

按生成配方至少完成一条代表性路径：检查前提 → Launch → Drive → Observe → Cleanup → 确认证据仍存在。失败迭代也清理自己创建的运行资源，不杀共享服务、不按进程名称批量杀进程。

用 [execution-contract](../engineering-run/references/execution-contract.md) 逐项记录状态。未实际运行的配方标为 draft / `NOT_VERIFIED`，不能说“接入完成”。报告已覆盖路径与尚未覆盖入口。

入口或命令变化时更新已有配方并复跑对应路径；产品回归与文档漂移分开处理。真实验证缺口解决后回到调用它的工程任务，不自动发布或 PR。
