---
{
  "id": "visitor-management-query",
  "slug": "visitor-management-query",
  "name": "访客管理查询 Skill",
  "description": "用于访客记录、访问统计与业务状态查询。",
  "skill_type": "custom",
  "category": "访客管理",
  "version": "1.0.0",
  "author": "CompKG-QA",
  "dir_path": "saves/skills/custom/visitor-management-query",
  "status": "draft",
  "enabled": false,
  "load_strategy": "triggered",
  "tool_dependencies": [
    "query"
  ],
  "mcp_dependencies": [],
  "skill_dependencies": [
    "rule-qa"
  ],
  "scenarios": [
    "组合业务场景",
    "管理分析",
    "结果交付"
  ],
  "call_example": "查询本周访客量并按来源渠道统计。",
  "params": {
    "top_k": 5,
    "temperature": 0.1,
    "trace": true,
    "timeout_ms": 10000
  }
}
---
# 访客管理查询 Skill

## 能力说明
用于访客记录、访问统计与业务状态查询。

## 调度规则
- Agent 负责意图识别、选择本 Skill、汇总结果，Skill 负责专门能力执行。
- 仅在问题匹配适用场景时激活，依赖缺失时返回可解释错误。
- 输出必须包含结构化结果、证据/计算过程、依赖状态。

## 输入输出约定
- 输入：用户问题、会话上下文、Agent 传入的 skill_params。
- 输出：answer、evidence、trace、warnings 四类字段。
