# Project Intake Checklist

Bootstrap 使用八个决策域。不要机械向用户逐项提问；能从仓库和上下文确认的先自动填写。

## Purpose

- 项目为什么存在？
- 主要用户/调用方是谁？
- 什么结果算成功？
- 是长期产品、内部工具、可复用库还是短期实验？

## Scope

- 核心能力是什么？
- 明确不做什么？
- 哪些功能应留给上层应用或外部基础设施？

## Architecture

- 核心领域边界是什么？
- 是否有公开 API / SDK / 协议？
- 哪些模块需要长期稳定？
- 哪些边界适合 Adapter / Provider 隔离？

## Runtime

- 支持平台、部署方式、运行周期。
- 是否有 daemon / server / CLI / library。
- 是否有 no-CGO、容器、sandbox 或本地环境约束。

## Dependencies

- 语言和版本。
- 依赖策略。
- 是否允许 framework。
- 哪些第三方系统属于外部依赖。

## Quality

- 单元、集成、E2E、平台测试需求。
- 本地快速检查入口。
- 合并前门禁。
- 是否需要 eval / benchmark / fixture。

## Safety

- 是否处理不可信输入。
- 是否执行 shell、文件写入、网络调用、数据库变更。
- 是否有密钥、个人数据、生产环境或资金风险。
- 哪些操作必须人工审批。

## Workflow

- Git / GitHub 是否使用。
- Issue / PR / CI / Release 策略。
- 分支与提交约定。
- 哪些状态必须保存在仓库外部的协作系统。
