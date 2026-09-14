---
name: project-adopt
description: Adopt an existing software repository into the personal Codex harness without overwriting its established conventions. Use when bringing a mature or unfamiliar repo under AGENTS/Skills/Hooks/verification conventions, auditing an existing harness, or incrementally adding missing engineering controls. Do not use for a new empty project; use project-bootstrap instead.
---

# Project Adopt

原则：先理解，再补缺口；不把个人模板强行覆盖到已有项目。

## 流程

1. 读取适用的现有 `AGENTS.md`、README、依赖清单、CI、Makefile/scripts 和关键 docs。
2. 识别现有 source of truth、工作流、门禁和项目特有约束。
3. 对照个人 Harness 做 gap analysis：
   - 已存在且有效
   - 已存在但冲突/过时
   - 缺失但有价值
   - 对项目不适用
4. 只提出最小接入方案。
5. 保留项目原有命名和成熟流程，除非它们确实造成问题。
6. 不自动新增大量目录、模板或空文件。
7. 如果需要新增项目 Skill，让它引用既有项目事实，不复制事实。
8. 如果需要新增 Hook，优先低歧义机械门禁，并确保脚本可单独测试。
9. 运行 Harness Doctor 或等价检查。
10. 输出 adopted / retained / deferred / unresolved。

## 冲突处理

个人规则与项目明确规则冲突时，以当前项目更具体的规则为准，并指出冲突，不静默覆盖。
