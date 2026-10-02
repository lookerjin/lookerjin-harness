# Field tests

本文件记录插件在真实项目上的试验结果。它是证据，不是 portable core。

来源：`refactor/agent-plugin-v2` @ `b1f576de`，随后在 `fix/field-test-hardening` 把重复摩擦做成机械约束。

## 001 experiment / bounded-retry

- Profile：`experiment`。未复制 Go Makefile / CI。
- Doctor 对插件仓在 Python 3.11 全绿；默认 3.10 会跳过 Profile 却 `status=pass`。
- 对业务仓跑 Doctor：`MISSING_PLUGIN`（符合设计）。
- change-review 预检能跑；未跟踪文件没有 diff。

## 002 go-service / portico

中等 HTTP 边缘网关，无第三方依赖。`make check` 在有代码后通过。纯 harness 空仓时 `go test ./...` 失败。CI 模板依赖人工替换 `REPLACE_WITH_FULL_COMMIT_SHA`。

## 003 go-library + go-service / rivulet

Redis Stream → MySQL + OpenTelemetry。`stdouttrace@v1.46` 把 Go 从 1.23 抬到 1.25。go-redis 默认多次重拨，和项目 Agent 重试政策不是同一层。替身测试不能当成真实 Redis/MySQL 已验证。

## 004 针对 001–003 的补强

已晋升到 portable core 的机械约束：

1. preflight 增加 `untracked_diff`。
2. Go Makefile 在没有 package 时 `make check` 跳过而不是失败。
3. `check-placeholders.py` 检查生成仓库残留 SHA 占位符；Doctor 检查模板必须保留占位符。
4. Doctor 在无法解析 TOML 时失败，不再 `status=pass`。
5. dependency-evaluation 与 engineering-defaults 补上语言下限、客户端 retry、验证等级。

明确不晋升：gateway/redis/otel profile、Docker/k8s 默认模板、Doctor 检查业务仓、golangci-lint/ORM/CDC/OTLP 默认。

## 005 轻量执行层 / synthetic CLI pilot

2026-10-02。先拉取并固定 pstack 0.15.5 的 `fae2c6ed95821bd85f614a73e4842e13229fa5e5`，再在现有 Harness 上实现候选。设计来源和边界见 [execution-core](execution-core.md)，父 Agent 的独立复跑记录与比较限制见 [execution-core-pilot.json](execution-core-pilot.json)。这是标准库 JSON CLI 夹具，不是真实生产项目证据。

- Doctor：12 个 Skill 可发现，零错误、零警告；Marketplace、既有 preflight/placeholder 自测通过。
- Eval 准备脚本：6 组 CLI 集成自测通过，覆盖同快照/不同版本、独立修改、已有输出拒绝、路径冲突、symlink、submodule 与非法 ref。
- 首轮独立评审发现 Git archive 副本没有 Git 基线，Change Review 无法采集 diff。修成独立本地 Git clone、检出原 commit、移除 origin、排除注入的 Skill 后，独立复跑 prepare → 修改副本 → preflight 通过；源仓库 HEAD/refs/status/config/exclude/内容均未变，无新 commit 或共享 alternates。
- 用相同自然任务、相同项目快照和继承的相同模型/工具做旧版/新版 Root Cause Debug 一对试验。两份都修复了 `get` 把整数零当缺键的问题。父 Agent 复跑基线失败及修复后 9 类 JSON 值和缺键路径，均符合契约。
- 版本盲判断者独立复跑精确 JSON 输出与缺键行为，两份产品修复等价；新版增加可重跑 CLI 测试与说明。新版测试对基线产生 7 处失败，修复后 3 个测试方法通过。两份初始项目产物均缺原始执行记录，不能据此确认执行者的历史执行，因此不把说明自报计为已验证。
- 因上述证据保存缺口，Root Cause Debug 与共同契约明确要求保存实际命令、退出码和必要原始输出。新上下文复测确实保留了修复前后 CLI 与测试的原始 JSON 记录：基线 6 个假值失败，修复后 2 个测试方法通过；父 Agent 再运行测试并确认临时存储为零。脱敏后的原始记录保存在同一证据文件。这是单次前测，不是新的配对收益结论，也不是对工具轨迹的认证审计。
- Verification Bootstrap 从仓库发现实际命令，生成项目局部配方/helper；父 Agent 复跑 21 个真实 CLI 动作：15 通过、6 失败。失败正是原应用的六种假值读取问题，helper 退出 1 并保留证据，没有修改产品或降低断言。临时数据清理、默认存储未创建和证据仍存在均已复核。
- Engineering Run 的只读调查路径解释了入口、磁盘转换与错误边界，未运行 CLI、未修改文件；父 Agent 确认工作区保持干净。

限制：只有一个小型配对与少量前测，不能证明整体收益、执行成本或跨项目有效性；无工具轨迹的历史行为标未确认。共享文件系统只实现上下文分离，非安全隔离。Design Explore、多 Unit Long Run、外部服务验证及跨客户端自动触发未运行，仍需真实项目验证。
