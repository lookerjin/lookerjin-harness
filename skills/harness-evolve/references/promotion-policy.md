# Harness Promotion Policy

个人 Harness 只保存已经通过真实开发证明有复用价值的东西。

## 可以提升到个人层的条件

至少满足一项：

1. 在两个或更多项目重复出现。
2. 在同一项目中已经被人工纠正 2～3 次。
3. 属于严重事故、高风险外部行为或数据破坏的防重复机制。
4. 能显著减少重复操作、上下文装载或人工判断。
5. 能写出清晰的 trigger、input、output 和 verification。

## 提升路径

```text
一次性问题
  -> 当前线程

项目反复出现
  -> Repo Skill / Repo AGENTS / Script

跨项目再次出现
  -> 个人 Harness 候选

真实验证有效
  -> 个人 Skill / Global AGENTS / Global Hook
```

## 降级或删除

出现以下情况时，优先删除或降级：

- 新模型已经稳定覆盖，Skill 只剩通用提示。
- Skill 触发频繁但很少改变结果。
- 规则与其他层重复并产生冲突。
- Hook 误拦截成本高于保护价值。
- 脚本维护成本超过它减少的重复劳动。
