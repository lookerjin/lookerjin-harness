# Profile Schema

V1 Profile 使用 TOML，方便 Python 标准库和 Codex 直接读取。

Profile 是**默认决策集合**，不是模板覆盖规则。

通用字段：

```toml
schema_version = 1
id = "profile-id"
description = "..."
extends = ["other-profile"]

[defaults]
# 该项目类型通常成立的默认判断

[recommended]
docs = []
skills = []
checks = []

[avoid]
items = []
```

使用原则：

- `extends` 表示语义继承，不要求自动做文件级合并。
- 多个 Profile 冲突时，以当前项目的明确证据和用户决定为准。
- `recommended` 只是触发考虑，不代表必须创建对应文件。
- Profile 中不要写某个具体项目的事实。
