---
name: project-adopt
description: Adopt an existing software repository into this portable engineering workflow without overwriting its established conventions. Use when bringing a mature or unfamiliar repo under AGENTS/Skills/verification conventions, auditing an existing harness, or incrementally adding missing engineering controls. Do not use for a new empty project; use project-bootstrap instead. Do not treat the target repo as this plugin, and do not run harness-doctor against it.
---

# Project Adopt

原则：先理解，再补缺口；不把插件模板强行覆盖到已有项目。

## 流程

1. 读取适用的现有 `AGENTS.md`、README、依赖清单、CI、Makefile/scripts 和关键 docs。
2. 识别现有 source of truth、工作流、门禁和项目特有约束。
3. 对照这套可移植工作方式做 gap analysis：
   - 已存在且有效
   - 已存在但冲突/过时
   - 缺失但有价值
   - 对项目不适用
4. 只提出最小接入方案。
5. 保留项目原有命名和成熟流程，除非它们确实造成问题。
6. 不自动新增大量目录、模板或空文件。
7. 如果需要新增项目 Skill，让它引用既有项目事实，不复制事实。
8. 不默认新增 Hook、客户端扩展或平行验证体系。只有当前客户端确实支持、且缺口属于低歧义机械约束时，才可以建议可选 adapter。
9. 不要对目标项目运行 `harness-doctor`。那个脚本只检查本插件仓库。
10. 按 `references/gap-output.md` 输出 adopted / retained / deferred / unresolved。

## 冲突处理

插件建议与项目明确规则冲突时，以当前项目更具体的规则为准，并指出冲突，不静默覆盖。
