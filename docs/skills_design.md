# CompKG-QA Skills 专业化设计说明

## 1. 设计目标

在不破坏现有 Agent、工具、MCP 与知识库配置的前提下，Skills 模块采用“文件系统存内容 + 配置/索引存元数据”的思路演进：

- `saves/skills/<skill_type>/<slug>/SKILL.md`：存放技能说明、提示词、使用规范与可选资源。
- Agent 配置中的 `skills`：存放当前智能体选择的 Skill slug 列表。
- Agent 配置中的 `skill_params`：存放每个 Skill 的运行参数。
- 前端 `skill_modules.js`：作为当前内置 Skill 元数据索引，后续可平滑迁移到数据库表。

## 2. 三类 Skill 分层

### 2.1 工具类 Skill（tool）

定位：通用原子能力。

包括：联网搜索、数学计算、时间查询、代码执行。

建议加载策略：常用轻量能力可预加载，外部接口、代码执行类能力按需懒加载，并启用超时、限流和沙箱。

### 2.2 业务类 Skill（business）

定位：项目核心业务能力。

包括：图谱查询、文档检索、规则问答。

建议加载策略：会话启动时随 Agent 配置进入 visible skills，真正触发时再加载工具/MCP依赖。

### 2.3 定制类 Skill（custom）

定位：业务场景组合能力。

包括：访客管理查询、数据统计、报表生成、多轮对话梳理。

建议加载策略：仅在用户触发对应场景时动态激活，允许编排工具类 + 业务类 Skill。

## 3. 标准元数据字段

每个 Skill 建议具备：

- `id` / `slug`：唯一标识。
- `name` / `description`：展示名称与能力说明。
- `skill_type`：`tool` / `business` / `custom`。
- `category`：细分类别。
- `version` / `author`：版本与维护方。
- `dir_path`：对应文件系统目录。
- `tool_dependencies` / `mcp_dependencies` / `skill_dependencies`：三类依赖声明。
- `scenarios` / `call_example`：适用场景与调用示例。
- `load_strategy`：`preload` / `lazy` / `session-visible` / `triggered`。
- `params`：运行参数，如 `top_k`、`temperature`、`trace`、`timeout_ms`、`retrieval_threshold`。

## 4. 渐进式加载建议

1. 会话启动：读取 Agent 配置的 `skills`，递归展开 `skill_dependencies`，构建可见技能集。
2. 技能激活：当用户意图命中某个 Skill，读取其 `SKILL.md` 并注入到上下文。
3. 按需加载：根据已激活 Skill 的 `tool_dependencies` 和 `mcp_dependencies` 动态挂载工具与 MCP 服务。

## 5. 安全与运维建议

- 工具类 Skill：对联网搜索、代码执行设置超时、限流、命令白名单和沙箱。
- 业务类 Skill：按知识库/图谱权限做访问隔离，避免越权查询。
- 定制类 Skill：按业务模块做角色可见性和数据行级权限控制。
- 监控指标：按 Skill 类型统计调用次数、成功率、平均耗时、异常日志与激活频率。