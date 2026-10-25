# 代码导航

地图服务当前问题。目标是减少重复探索，并让人能核对关系；全量图大小不是质量指标。

## 选路与生命周期

| 当前问题 | 最小路径 |
|---|---|
| 找错误字符串、配置项、已知入口 | `rg` 后读必要上下文，不建图 |
| 谁引用/实现/调用一个符号 | 可用的 LSP/符号工具；退到 AST，再退到文本追踪。标注别名、动态分派等未确认边界 |
| 跨模块改动影响谁、用户要看关系 | 范围内提取关系 → 反向查询 → 核对入口与验证 → 同源 JSON / draw.io |
| 理解领域概念或设计动机 | 项目已有术语、模块导航、ADR；缺失时按需记录到既有位置，不预建文档体系 |

Design 用局部图讨论边界与状态；Plan 连接改动影响和已有验收；Execute 查询当前路径；Verify 选相关真实入口测试。地图不决定要不要走六阶段，也不证明运行行为。

## 可运行入口

Python 3.11+，脚本只用标准库。以下 `MAP` 指向本 Skill 的 `scripts/code-map.py`，`ROOT` 是目标项目根，输出目录放在观察范围外。使用实际路径替换示例；不要把示例变成目标项目固定目录。

```bash
python "$MAP" build --root "$ROOT" --scope src --extractor /path/to/depcruise --output /tmp/navigation/map.json
python "$MAP" status --root "$ROOT" --input /tmp/navigation/map.json
python "$MAP" query --root "$ROOT" --input /tmp/navigation/map.json --node src/auth.js --direction in --depth 2 --limit 30
python "$MAP" drawio --root "$ROOT" --input /tmp/navigation/map.json --node src/auth.js --direction in --depth 2 --limit 30 --output /tmp/navigation/auth.drawio
```

`--scope` 可重复；节点 ID 精确匹配，`in` 找依赖/调用该节点的路径，`out` 找它依赖/调用的路径；`both` 看两侧。图中箭头始终保留原关系方向。`--kind calls` 等可过滤关系种类。限制的是边数，不是 token 数；输出明确 `truncated` 和 `omitted_edges`，不能把截断查询当完整影响面。

`status` / `query` 过期退出 2，错误退出 1；`drawio` / `record` 拒绝过期输入。输出文件必须是新路径，失败不覆盖历史产物。观察范围内最多 5000 个文件、每文件 8 MiB，超限先缩小范围。Git 项目遵循忽略规则，额外跳过依赖/缓存目录；子模块、忽略文件、范围外配置与消费者不在新鲜度保证内。Symlink 输入拒绝处理。

### JS / TS 模块依赖

`build` 调用 **dependency-cruiser**，经测试版本 **18.7.0**（MIT；Node `^22 || ^24 || >=26`）。优先复用项目已固定的工具；缺失且确需建图时，可在临时工具目录安装固定版本：

```bash
npm install --prefix "$TOOL_DIR" --ignore-scripts --no-audit --no-fund dependency-cruiser@18.7.0
```

维护来源与 CLI 文档：[dependency-cruiser](https://github.com/sverweij/dependency-cruiser)。当前版本直接依赖 Acorn 解析、enhanced-resolve 等组件；不把其实现复制到 Harness。安装在工具目录，不抬升目标项目 Node 版本；不满足运行时就采用已有能力。依赖仅用于这一可选路径，不加入默认启动或 MCP。

适配器显式关闭项目可执行配置和缓存，提取局部 imports；保存工具版本和未解析依赖，提取前后核对源码。配置驱动的路径别名、框架路由和 TS 编译选项可能不完整；存在这些条件时使用项目原有配置/语言服务做查询，并按下面的记录入口接入。不得据默认适配器结果断言所有引用已覆盖。TS 项目需项目工具具备相应解析支持；本轮实测覆盖 JS/MJS，不宣称已验证全部 TS 工具链。

## 接入符号查询与源码观察

先用 `snapshot --root ... --scope ... --output ...` 固定读取前的内容基线，再在该 JSON 的 `nodes` / `edges` 填入实际工具结果或源码观察，最后用 `record --root ... --input ... --output ...` 核对后存新文件。不要为旧结果重拍基线：变化后重新查询/阅读对应关系。没有工具证据就记录未知，不能按函数名猜调用。

节点：`id`、`label`、`path`；范围外节点用 `boundary: true` 并说明边界。关系形状：

```json
{
  "source": "src/checkout.js#checkout",
  "target": "src/payment.js#charge",
  "kind": "calls",
  "basis": "observed",
  "evidence": [{"path": "src/checkout.js", "line": 42}],
  "acceptance_ids": ["payment-success"]
}
```

`basis`：`static` 为解析工具输出，`observed` 为明确源码观察，`inferred` 为待验证推断（图中虚线）。`observed` 不代表运行验证。允许的关系为 imports / calls / data-flow / state-transition / verifies。非 imports 关系必须给出源码行；imports 适配器保留文件和 import specifier，不伪造行号。语义是否正确仍须审阅源码，检查器只核对结构与新鲜度。

给图起与问题一致的范围，交付 draw.io 文件及对应局部 JSON，附未覆盖边界。节点用人能理解的标签，证据留文件路径；需要真实运行证明时回到验证配方。不要另建验收数据库：`acceptance_ids` 引用项目已有索引，修改/共享状态/动态边界仍要人工检查。

## 维护

复用前检查内容指纹；HEAD 变化而本范围内容未变不会误报过期，HEAD 未变但文件修改会过期。新增文件也会使观察范围过期，防止新增调用者漏入旧地图。源码修正后保存新产物，旧图不擦除。

当前不安装更新 hook。只有实际重复使用证明值得自动维护、且宿主提供受支持入口时，才设计显式开启、范围限定、失败保留旧产物的更新机制。地图失效不阻断普通搜索与开发。
