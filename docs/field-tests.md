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
