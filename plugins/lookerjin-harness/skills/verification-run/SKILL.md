---
name: verification-run
description: Execute an existing project verification recipe against the real caller surface and assess evidence for the requested behavior. Use after a change, to reproduce a result, or to explicitly audit and maintain verification coverage. Distinguish runtime evidence, model checks, and record integrity. Missing recipes go back to the coordinator for verification-bootstrap; this skill does not redesign product code or auto-publish.
---

# Verification Run

读 [执行契约](../engineering-run/references/execution-contract.md) 和项目权威配方。配方缺失时报告缺少哪个入口/动作，由调用方选择一次性检查或 Verification Bootstrap，避免相互递归。

## 日常 Run

1. 固定目标验收、受影响入口、当前源码/产物与环境前提。由真实调用链映射影响范围，包含共享状态、错误、并发与副作用；不能只按改过的文件挑测试。已有有效证据可复用并说明适用性。若已有 [局部地图](../system-understand/references/code-navigation.md)，先查新鲜度，再反向查询改动节点、连接已有验收 ID；过期、截断或仅 imports 的结果不能证明调用者覆盖，补查动态边界与共享状态。简单任务不为选择测试而强制建图。
2. 读项目的 [配方结构](../verification-bootstrap/references/recipe-shape.md)，确认前提与正确实例；实际 Launch → Drive → Observe。断言内容、状态转换与副作用，不能只看 exit 0 / HTTP 200 / 构建成功。
3. 先做代表性路径，失败时辨别产品缺陷、配方漂移、环境阻塞、观察不足。产品缺陷返回 Execute / Root Cause Debug；只修本次必要配方缺口不扩大产品范围。针对实际失败保留原始记录。
4. 正常与失败退出都清理自己拥有的实例/数据，证据必须在清理后存在。不得杀共享服务或覆盖用户数据。
5. 输出逐项证据和未覆盖边界。关键验收必须全部 VERIFIED；NOT_RUN、FAILED、INCONCLUSIVE 分开记录。需要机器核对时按 [证据输入](references/evidence-format.md) 使用 [check-evidence.py](scripts/check-evidence.py)，该脚本只证明记录完整性与文件指纹一致，不替代运行和语义判断。

## 显式 Maintain

用户要求完整维护，或覆盖图与实现明显漂移时，使用 [维护流程](references/maintenance.md)。日常 Run 只覆盖本任务影响面，不能声称全配方同步；Maintain 核对完整声明覆盖面并记录同步基线。

高影响状态不变量、并发或协议可按 [形式化检查](references/formal-checks.md) 增补模型与负对照。模型证明、真实入口观察和静态检查分别报告。

返回验收状态、证据、缺口及应回到的阶段；不通过删断言、降低门槛、扩大忽略规则或把失败改成预期成功获得绿色结果。
