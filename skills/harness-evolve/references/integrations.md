# Integrations Policy

## 默认保留

### GitHub

用途：

- Issue：任务与需求状态。
- PR：变更审查与协作状态。
- CI：远端确定性门禁。
- Review：外部协作反馈。

本地 Git 状态仍以仓库本身为准。

### Context7 MCP

只在以下场景使用：

- 外部库 / SDK / API 当前版本。
- 模型知识可能过时的框架行为。
- 需要对照官方示例或版本差异。

不用于：

- 项目内部代码导航。
- 标准库常识。
- 已经由项目权威文档定义的事实。

### Codex Browser

优先用于：

- localhost 功能验证。
- UI 点击、输入、导航。
- DOM、Console、Network 和真实交互调试。

只有当验证需要成为可重复的 E2E 或 CI 门禁时，再引入 Playwright 等测试框架。

## 不默认安装

Serena、Beads、RTK、Caveman、Linear、大型 Skill Pack 等不作为个人默认层。

先通过真实使用证明存在以下瓶颈再引入：

- 代码库规模导致原生导航明显不足。
- 跨 Session / 多 Agent 任务依赖无法由 GitHub 等现有状态系统表达。
- CLI 输出经过 profiling 证明是主要 token 成本。
- 现有工作流在多个项目稳定重复。
