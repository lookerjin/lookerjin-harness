# lookerjin-harness

个人 AI 开发 Harness，用来把跨项目复用的开发规则、Skills、Hooks、Profiles、验证脚本和项目初始化流程沉淀成一套可持续演化的工程系统。

它不是项目模板，也不要求所有项目使用同一套技术栈。核心目标是：**让 AI 在进入一个项目时知道长期规则、按需加载工作流、调用确定性工具完成验证，并把项目事实和执行状态放在正确的位置。**

## 架构

```text
lookerjin-harness/
├── global/
│   ├── AGENTS.md          # 跨项目长期规则
│   ├── config.toml        # Codex 配置基线
│   ├── hooks/             # 用户级机械约束与收口检查
│   └── rules/             # Harness 自身的职责边界
│
├── skills/                # 跨项目可复用工作流
│   ├── project-bootstrap/
│   ├── project-adopt/
│   ├── root-cause-debug/
│   ├── dependency-evaluation/
│   ├── change-review/
│   └── harness-evolve/
│
├── profiles/              # 不同项目类型的默认决策集合
│   ├── go-library/
│   ├── go-service/
│   ├── agent-core/
│   ├── web-app/
│   └── experiment/
│
├── assets/                # 可按需复制到项目中的工程资产
│   ├── agents/
│   ├── github/
│   ├── makefile/
│   └── scripts/
│
└── checks/
    └── harness-doctor/    # Harness 自检
```

职责保持简单：

```text
长期规则       -> AGENTS.md
任务流程       -> Skill
机械约束       -> Hook
确定性执行     -> Script / Makefile / CI
项目事实       -> Docs / Code / Config
任务状态       -> GitHub Issue / PR / Roadmap
外部能力       -> MCP / Plugin / Browser
项目默认决策   -> Profile
```

## 安装

### 推荐：直接交给 AI

把仓库地址发给 Codex 或其他具备本地文件和终端能力的 Coding Agent：

```text
https://github.com/lookerjin/lookerjin-harness
```

然后告诉它：

```text
安装并接入这个个人 Harness。

先阅读仓库 README 和安装脚本，检查当前环境与已有 Codex 配置。
不要覆盖我已有的 AGENTS.md、config.toml、hooks.json 或 Skills。
先执行 dry-run，说明会新增什么、哪些地方有冲突；确认没有破坏性覆盖后完成安装。
安装后运行 Harness Doctor，并报告已安装、跳过、冲突和未验证项。
```

AI 应完成的流程：

```text
读取仓库
  ↓
检查当前环境
  ↓
检查 ~/.codex 和 ~/.agents
  ↓
执行安装 dry-run
  ↓
处理或报告冲突
  ↓
安装个人层
  ↓
运行 Harness Doctor
  ↓
报告最终状态
```

安装脚本默认不会覆盖已有文件。

### 手动安装

先预览：

```bash
python assets/scripts/install-user.py
```

确认后执行：

```bash
python assets/scripts/install-user.py --apply
```

默认行为：

- `global/AGENTS.md` -> `~/.codex/AGENTS.md`
- `global/config.toml` -> `~/.codex/config.toml`
- `global/hooks/` -> `~/.codex/hooks/` 与 `~/.codex/hooks.json`
- `skills/*` -> `~/.agents/skills/*`
- 已存在的目标文件不会被覆盖
- Unix 默认优先使用 Skill 符号链接，Windows 默认复制

安装后可运行：

```bash
python checks/harness-doctor/doctor.py --root .
```

## 怎么用

### 新项目

在新项目目录中让 Codex 使用：

```text
$project-bootstrap
```

它会先扫描项目和用户描述，建立 Project Intake，并把关键判断标记为：

- `confirmed`：有直接证据确认
- `inferred`：根据现有证据推断
- `unknown`：当前无法可靠确定且可能影响设计
- `N/A`：当前项目不适用

然后选择合适的 Profile，只创建项目真正需要的 Harness：AGENTS、Docs、项目级 Skills、Hooks、Makefile、Scripts、CI 等。

### 已有项目

```text
$project-adopt
```

流程是：

```text
scan
  ↓
理解现有工程体系
  ↓
gap analysis
  ↓
minimal adoption
```

不会机械覆盖已有项目规范，也不会为了统一目录而重构项目。

### 日常开发

```text
$root-cause-debug
```

用于系统化排障：证据 -> 假设 -> 最小实验 -> 根因 -> 修复 -> 回归验证。

```text
$dependency-evaluation
```

用于新增依赖、自研基础设施或技术选型前的评估。

```text
$change-review
```

用于实现结束后的 diff、测试证据、未追踪文件、文档同步和未验证项检查。

```text
$harness-evolve
```

用于回顾真实开发过程，把已经稳定重复出现的规则或流程提升到个人 Harness，同时清理失效或重复能力。

## Profiles

Profile 不是 starter repo，而是一组默认决策。

例如：

```text
go-library
    +
agent-core
```

可以组合成一个强调公共 API、状态持久化、恢复、安全边界、Provider 隔离和评测能力的 Agent Core 项目。

当前 Profiles：

- `go-library`：可复用 Go 库
- `go-service`：长期运行的 Go 后端服务
- `agent-core`：Agent Runtime / Core / Harness
- `web-app`：需要真实浏览器验证的 Web 应用
- `experiment`：短生命周期、低成本验证项目

真实项目证据始终高于 Profile 默认值。

## 项目级 Harness

个人 Harness 只保存跨项目复用的能力。

进入具体项目后，项目自己的规则和流程仍然放在项目仓库中：

```text
project/
├── AGENTS.md
├── .agents/skills/
├── .codex/
├── docs/
├── scripts/
├── Makefile
└── .github/
```

原则是：

- 个人层描述“我通常怎么开发”
- 项目层描述“这个项目必须怎么运行”
- 能机械验证的事情尽量不要只靠模型记住
- 同一类事实只保留一个权威来源

## 外部能力

默认保持精简：

- GitHub：Issue、PR、CI 和远端状态
- Context7：外部库、SDK、API 和版本文档
- Codex Browser / CDP：交互式 Web 验证

只有真实项目出现明确需求时，再引入额外 MCP、代码索引、任务系统或 Token 优化工具。

## 演化

这套 Harness 不是一次设计完成的。

新的规则或流程进入个人层之前，优先满足至少一个条件：

1. 已经在多个项目重复出现
2. 同一个项目被重复人工纠正多次
3. 属于高风险问题的确定性防护
4. 能明显减少重复操作或认知负担
5. 可以定义清晰的触发条件、输入、输出和验证方法

先在真实项目中运行，再决定是否沉淀。