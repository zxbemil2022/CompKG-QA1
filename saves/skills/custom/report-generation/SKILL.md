---
{
  "id": "report-generation",
  "slug": "report-generation",
  "name": "报表生成 Skill",
  "description": "用于 SQL 查询报表、Markdown 报告和可视化图表输出。",
  "skill_type": "custom",
  "category": "报表生成",
  "version": "1.0.0",
  "author": "CompKG-QA",
  "dir_path": "saves/skills/custom/report-generation",
  "status": "ready",
  "enabled": false,
  "load_strategy": "triggered",
  "tool_dependencies": [
    "query",
    "execute_modify"
  ],
  "mcp_dependencies": [
    "mcp-server-chart"
  ],
  "skill_dependencies": [
    "data-stat-analysis"
  ],
  "scenarios": [
    "组合业务场景",
    "管理分析",
    "结果交付"
  ],
  "call_example": "生成近 30 天知识库使用情况周报。",
  "params": {
    "top_k": 5,
    "temperature": 0.1,
    "trace": true,
    "timeout_ms": 10000
  }
}
---
# 报表生成 Skill

## 能力说明
用于 SQL 查询报表、Markdown 报告和可视化图表输出。

## 调度规则
- Agent 负责意图识别、选择本 Skill、汇总结果，Skill 负责专门能力执行。
- 仅在问题匹配适用场景时激活，依赖缺失时返回可解释错误。
- 输出必须包含结构化结果、证据/计算过程、依赖状态。

## 输入输出约定
- 输入：用户问题、会话上下文、Agent 传入的 skill_params。
- 输出：answer、evidence、trace、warnings 四类字段。