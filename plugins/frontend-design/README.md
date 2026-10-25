# Frontend Design

独立 UI 设计专家，处理页面视觉方向、排版、布局和内容表达。由当前工程任务按需使用，普通功能修复不要求重新设计页面；工程生命周期和实际行为验收由 Harness 负责。

直接描述需求，例如“给这个工作室做课程预约页”或“保持品牌不变，改善这个页面的信息层级”。技能仍可通过宿主实际提供的手动入口调用，不依赖某种斜杠别名。

这个包只包含一个 [frontend-design](skills/frontend-design/SKILL.md) 技能，无 hook、MCP、后台进程或安装依赖。Marketplace 可发现不代表客户端已启用；启用后使用宿主的技能发现能力，或读取安装目录中的技能文件。浏览器截图和交互验证由环境已有工具提供。

技能来自 Anthropic，正文和许可证保持原样，具体提交及校验值见 [SOURCE.json](SOURCE.json)。遵循 [Apache-2.0](LICENSE)，技能目录内同时保留其 [许可证](skills/frontend-design/LICENSE.txt)。本地包装版本 `0.1.0` 不代表原技能发布版本，也不表示本包由 Anthropic 发布或背书。

本地只增加 Codex 兼容 manifest 和分发说明；普通 Skill 文件仍可被其他支持该格式的客户端读取。自测：在 Marketplace 仓库根运行 `python scripts/frontend_design_test.py`。
