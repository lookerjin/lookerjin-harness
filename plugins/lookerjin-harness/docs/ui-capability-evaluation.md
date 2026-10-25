# UI 能力评估

本报告记录引入前的候选筛选；后续已将 Frontend Design 固定版本作为独立本地插件加入 Marketplace，并完成配对行为试验。当前状态与结果见 [集成与 A/B 记录](frontend-design-ab.md)。下文“未安装/未加入”均指本报告当次检查状态。

2026-10-25。结论：UI 值得作为独立专家类别接入；六阶段、授权、协作、恢复与交付判断仍由当前 Harness 负责。本轮完成源码检查、局部运行和接入契约，未安装用户端技能、未改 Marketplace 成员、未引入 hook。以下推荐是下一步选型，不是已经通过跨项目效果评估。

## 候选与实际文件

| 候选与检查版本 | 具体能力与文件 | 成本、边界与判断 |
|---|---|---|
| [Frontend Design](https://github.com/anthropics/skills/tree/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/frontend-design)，提交 2026-10-09 | `skills/frontend-design/SKILL.md`：从实际主题形成视觉方向，先审设计计划再实现，布局/字体/内容/截图自查；同目录 `LICENSE.txt` 为 Apache-2.0 | 入口正文 9,390 字节，无附加脚本运行时。适合首先试用的设计专家；没有自动规则检测器。本轮仅源码检查，没有证明它比其他技能生成的设计更好 |
| [Web Design Guidelines](https://github.com/vercel-labs/agent-skills/tree/063bee94c3f4df8453406c830b0a7df0f2860278/skills/web-design-guidelines)，提交 2026-08-28 | `SKILL.md` 加 [规则文件](https://github.com/vercel-labs/web-interface-guidelines/blob/434b7f91364665f2f733b310ec54809bf8f37937/command.md)：语义、焦点、表单、动画、响应和性能审查 | 入口 1,231 字节，规则 8,055 字节；适合代码审查补充。默认每次取 `main`，只固定入口仍会漂移，须记录实际规则版本。README 声明 MIT，但检查版本无完整根 LICENSE 文件，正式再分发前补齐许可依据；本轮未复制其内容 |
| [Impeccable](https://github.com/pbakaus/impeccable/tree/936867543ac2576920d663cc9803597f6044f3ac)，源码 4.7.1、提交 2026-10-23 | `plugin/skills/impeccable/SKILL.md`、`reference/craft-floor.md`、`reference/new-work.md`；`cli/bin/cli.js` 启动原生检测器；`crates/html/` 静态分析，`browser-bundle/` 浏览器观察；Apache-2.0 | 入口 12,042 字节，craft floor 4,516 字节，其他资料按需。手动 `detect` 不需要 hook，但完整插件含 hook 配置，不能整包默认安装。本轮直接测 Linux 原生引擎 0.1.17，安装目录 43,700,941 字节。适合以后需要更强设计诊断时试用，不作为默认 UI 总管 |
| [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/tree/d14efff8ed1faa4187f004f79926f428c8074ec7)，2.15.0、提交 2026-10-23 | `.claude/skills/ui-ux-pro-max/SKILL.md`；`src/ui-ux-pro-max/scripts/search.py`、`core.py`、`design_system.py` 与 `data/*.csv`：本地 BM25 规则检索、设计推荐与多平台指南；MIT | 已生成入口 15,969 字节；模板 27,433 字节不能当成实际入口负担。检索仅需 Python 标准库，适合按问题取规则；检索命中不等于语义满足，不能据此自动决定设计或通过验收 |

仓库采用量只作成熟度参考：当日 GitHub 页面显示 Impeccable 约 86.4k stars、UI/UX Pro Max 约 140k stars；最终判断仍依赖代码、维护、试验与适用范围。DeepWiki 对 Impeccable 的索引停在 4.7.0，涉及当前行为以已检出的文件为准。

发布渠道也要分开核对：源码标记 4.7.1，但当日 npm `impeccable@4.7.1` 返回 ETARGET，查询 npm 当前为 4.7.0。本轮没有默默替换成旧整包，而是按源码声明固定安装已存在的 `@impeccable/cli-linux-x64@0.1.17`，仅运行检测器。其安装耗时 0.831 秒，首次失败尝试 0.478 秒也保留；不将此视为完整技能安装成功。

## 局部试验：质量、时间与成本

原始样本、命令、退出码、输出指纹、输入 HTML 及版本见 [ui-capability-checks.json](ui-capability-checks.json)。除缺失文件负对照为一次外，每项 5 次，以下为 wall time 中位数；保留首样本，不清空 OS 缓存。

| 场景 | 实际观察 | 单次耗时与输出 |
|---|---|---|
| 查询表单错误摘要规则 | Top 3 包含聚焦错误摘要、字段链接与内联错误；语义相关 | 0.048 秒，JSON 1,903 字节 |
| 查询弹窗焦点陷阱/关闭后恢复 | 初次及一次改写均只有泛化焦点建议；没有查到可核实答案 | 0.044 / 0.045 秒，分别 1,812 / 1,778 字节 |
| 无匹配词 | `count=0` 明确无命中；进程仍退出 0 | 0.052 秒，134 字节 |
| 静态负对照：低对比度、小字号 | 检出 low-contrast、tiny-text、undersized-ui-text，退出 2 | 0.031 秒，5,916 字节 |
| 缺失输入文件 | stdout 同样可为 `[]`，但退出 1、stderr 报操作失败；不可标为无问题 | 0.002 秒，单次 |
| 表单缺少错误摘要聚焦 | 静态检测 5 次均 `[]` / exit 0；浏览器操作 5 次均 9/10，聚焦项失败 | 静态 0.028 秒；浏览器 0.446 秒 |
| 同表单补上聚焦 | 静态结果仍 `[]`；浏览器 5 次均 10/10 | 静态 0.028 秒；浏览器 0.426 秒 |

浏览器检查包含无效输入的摘要可见性与聚焦、字段错误关联、错误链接定位、有效输入后的成功提示与错误清除、320/768/1440 宽度溢出及 pageerror。启动 Chromium 单独耗时 0.172 秒，之后每个样本创建新 context。环境拒绝 `file://` 导航，首次运行记为 INCONCLUSIVE；改用 `set_content` 渲染自有 HTML，没有修改浏览器策略。这证明此受控页面的交互，不证明部署 URL、后端保存、屏幕阅读器或真机效果。

本地检索与检测脚本没有调用外部模型 API；整个 Agent 任务的模型 usage 和金额不可得，记录为 unknown。文件字节、安装体积、CLI 耗时均不转换成 token 或金额。本轮不是盲评，不据此宣称审美提升或 Agent 总成本下降。

## 接入次序

1. 先选一个设计专家试用，优先轻量 Frontend Design；保留项目现有视觉约束，普通组件修复直接 Execute → Verify。
2. 已有 UI 需要审查时才加载对应规则；需要具体方案资料时才使用本地检索，不同时加载多个大而全的设计技能。
3. 实现继续使用项目技术栈和组件库。按 [UI 接入契约](../skills/engineering-run/references/ui-capabilities.md) 将真实入口与验收 ID 返回 Verification Run；静态工具不能替代浏览器操作。
4. 若反复需要自动视觉诊断，再试 Impeccable 的固定版本手动检测路径。不要注册它的 hook，不引入 live 注入或整套子命令作为用户必经入口。
5. 当前候选包含普通 Skill 和客户端专用 Plugin 包，不能把任意技能目录直接登记为 Codex Plugin。正式分发前检查目标宿主兼容包、固定引用、许可证及资源相对路径；本轮 Marketplace 未变，也未制作副本或空插件。

原生移动端、桌面端以及跨页面复杂交互尚未实测；本报告的可运行结论限于 Web 表单与局部工具探针。
