# lookerjin-harness

一个面向 AI Coding Agent 的软件工程 Domain Harness，以 Codex Plugin 形式分发。

它负责跨项目可复用的软件工程工作流、验证方式和演化方法；具体语言、框架或工具的专业知识优先交给独立 Expert Plugin，而不是继续膨胀本 Harness。

本插件位于 Marketplace 仓库的：

```text
plugins/lookerjin-harness/
```

## 定位

`lookerjin-harness` 负责软件工程领域的任务路由、能力组合、验收与反馈。Domain Harness 是架构角色，不是新的协议类型；它在本领域收敛专业能力的结果。

它主要回答：

- 项目应该怎样初始化或接入；
- 一类工程任务应该怎样从意图推进到可信结果；
- 问题应该怎样定位根因；
- 新依赖应该怎样评估；
- 变更应该怎样审查和验证；
- 哪些重复摩擦值得沉淀进 Harness；
- 哪些问题应该交给独立专家插件或外部工具。

它不试图成为 Go、Python、TypeScript、数据库、安全或前端知识大全。

## 架构

```text
lookerjin-harness/
├── .codex-plugin/
│   └── plugin.json
├── assets/
│   ├── logo.svg
│   └── composer-icon.svg
├── mcp.json
├── AGENTS.md
├── docs/
└── skills/
    ├── engineering-run/
    ├── system-understand/
    ├── design-explore/
    ├── verification-bootstrap/
    ├── project-bootstrap/
    ├── project-adopt/
    ├── root-cause-debug/
    ├── dependency-evaluation/
    ├── change-review/
    ├── harness-evolve/
    ├── harness-eval/
    └── harness-doctor/
```

`.codex-plugin/plugin.json` 是本插件唯一的 Codex manifest。根目录不再维护第二份 `plugin.json`，避免重复事实和版本漂移。

`assets/` 是插件级展示资源目录，供 Codex manifest 中的 `logo`、`composerIcon` 等字段引用。

`docs/` 只是插件级文档和实地验证记录，不参与插件发现。

根目录 `AGENTS.md` 只约束如何修改本插件，不会自动成为目标项目的规则。

## Skills

- `engineering-run`：任务入口。按意图选择 investigate / feature / bug-fix / refactor / prototype / long-run；Playbook 是该 Skill 的 references，不是顶层协议。
- `system-understand`：追踪入口、转换、状态与依赖；涉及隐藏约束时按需查询决策历史。
- `design-explore`：比较结构不同的方案，用共同标准与低成本实验收敛；不要求多模型或多 Agent。
- `verification-bootstrap`：复用或建立项目级 launch/drive/observe/cleanup 配方，实际跑一条代表性路径；未运行的配方保留 draft 标记。
- `project-bootstrap`：为新项目建立最小可演化 Harness。先列出将创建的文件，再写入。
- `project-adopt`：把已有项目接入这套工作方式，先理解再最小改造。不要默认改造成插件，也不要默认跑插件 Doctor。
- `root-cause-debug`：证据 -> 假设 -> 最小实验 -> 根因 -> 修复 -> 回归验证。
- `dependency-evaluation`：新增/替换依赖或准备自研通用基础设施时使用。
- `change-review`：领域变更验收入口。预检后按需使用专业审查，核对范围、行为、测试证据和未验证项；OCR 组合约定按需读取，不重复维护专业规则。
- `harness-evolve`：从真实项目的重复摩擦中决定哪些能力应该沉淀、迁移、集成或删除。没有重复证据就停止。
- `harness-eval`：相同任务与隔离产物的版本盲评；附准备快照的脚本，脚本本身不执行 Agent 或评分。
- `harness-doctor`：只检查本插件目录。需要 Python 3.11+；对着业务仓跑会失败。

## 执行与证据

入口路由 → Playbook → 所需能力 → 项目真实验证 → 变更审查。简单任务直接用具体 Skill，复杂任务才加载更多阶段。共同证据语义与授权边界由 [execution-contract](skills/engineering-run/references/execution-contract.md) 定义。

Harness 定义如何推进和什么算证据；项目层保存具体运行事实与配方；Expert Plugin 提供专业知识；MCP/工具提供外部能力。子 Agent、多模型和并行取决于当前客户端能力与规则，没有这些也可以顺序完成。

Doctor 检查结构，Eval 检查行为，Evolve 判断经验是否值得长期保留。三者不能互相替代。新执行层是本次明确设计的待验证候选，不能因为结构检查或少量夹具通过就声称已跨项目验证。

架构图、泳道用户旅程以及设计参考与取舍见 [docs/execution-core.md](docs/execution-core.md)，实际运行记录仍统一保存在 [docs/field-tests.md](docs/field-tests.md)。

## Context7 MCP

`mcp.json` 声明 Context7 的远程 Streamable HTTP 服务：

```text
https://mcp.context7.com/mcp
```

插件不保存 API Key。需要更高额度或认证能力时，由当前 Agent 客户端自己的认证机制管理凭证。

## Project Bootstrap Resources

Profile、工程默认值和项目模板属于 `project-bootstrap` Skill 的渐进式资源：

```text
skills/project-bootstrap/
├── SKILL.md
├── references/
│   ├── intake-checklist.md
│   ├── engineering-defaults.md
│   └── profiles/
└── assets/
    ├── AGENTS.repo.template.md
    ├── github/
    └── makefile/
```

`engineering-defaults.md` 是项目规则素材的唯一来源。只有初始化项目时才读取这些内容，并按项目裁剪后写入目标仓库 `AGENTS.md`。

## 能力归属

发现新的限制、规则、工具或专业能力时，不要默认加入 Harness。

```text
New Capability / Constraint
        │
        ▼
是一次性的吗？
   │         │
  是         否
   │         │
Prompt       ▼
         属于当前项目？
          │        │
         是        不确定 / 可能复用
          │        │
          ▼        ▼
    Project Layer  先在真实项目运行
                         │
                    多次重复验证？
                     │         │
                    否         是
                     │         │
                  保持局部      ▼
                          已有成熟能力？
                           │         │
                          是         否
                           │         │
                           ▼         ▼
                      Expert Plugin  再判断是否进入
                      / Tool / MCP   Harness core
```

Harness 应优先拥有“怎么做事”的稳定方法，而不是拥有所有“具体怎么实现”的专业知识。

## 与 Expert Plugin 的关系

本插件不声明 Plugin 依赖，也不定义 Plugin-to-Plugin 调用协议。

Developer 领域的专业插件由 Marketplace / Client / Agent Environment 组合使用。例如现代 Go、数据库、安全或前端能力可以作为独立 Expert Plugin 与本 Harness 共存。

Harness 负责软件工程领域工作流和验收；Expert Plugin 负责专业能力；Tool / MCP 负责执行或外部知识访问。

市场中的 `open-code-review-codex` 是独立的专业审查插件。默认优先委托模式，当前 Agent 使用 OCR 文件选择与规则完成审查；完整模式需要已选择并配置好的外部模型。Change Review 保留覆盖核对、项目真实验证和 findings 最终判断。CLI 不可用时保持可用的领域审查并报告缺口。详细约定见 [OCR 适配](skills/change-review/references/open-code-review.md)，运行证据见 [field-tests](docs/field-tests.md)。

## 使用原则

- 项目长期规则进入项目 `AGENTS.md`。
- 特定任务流程进入 Agent Skill。
- 可确定性执行的检查进入项目 Script / Makefile / CI。
- 外部当前知识通过 MCP 或专业插件获取。
- 项目事实保留在项目 Docs / Code / Config。
- 任务状态保留在 Issue / PR / Roadmap。
- 同一类事实只保留一个权威来源。
- 成熟开源能力优先集成，不为“自有”而重复实现。

这套 Harness 通过真实项目持续演化，不追求一次设计完整。实地记录见 [docs/field-tests.md](docs/field-tests.md)。
