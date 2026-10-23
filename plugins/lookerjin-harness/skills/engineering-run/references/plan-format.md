# 可选 Unit 导出格式

复杂计划可把现有状态临时导出为 JSON，运行 `python <skill>/scripts/check-plan.py <plan.json>`。不为小修改强制持久化；此导出不取代项目权威计划。

```json
{
  "version": 1,
  "units": [{
    "id": "compat-entry",
    "goal": "增加兼容入口，保持公开行为",
    "scope": ["src/api.py"],
    "context": ["现有调用者及行为基线的位置"],
    "acceptance": ["旧调用返回值与副作用保持"],
    "verify": ["运行真实公开入口的兼容用例"],
    "depends_on": [],
    "status": "pending"
  }]
}
```

状态为 pending / active / verified / blocked；verified 必须带非空 `evidence` 引用数组，blocked 必须带 `blocker`。active 与 verified 的依赖必须 verified。验证引用仍需负责人核对，检查器不会读它们或把引用当成真证明。

退出 0 表示结构与显式依赖有效；`ready` 是 pending 中前置全 verified 的项，不表示获得并行/执行授权。`scope_overlaps` 只检测同名范围，不分析父目录、别名、共享实例、隐式依赖或实际写入；需人工/Agent 判断隔离。循环、未知依赖、重复 ID 或缺少验收等返回 1，失败时不提供就绪集。
