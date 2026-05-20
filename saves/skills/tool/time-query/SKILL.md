---
{
  "id": "time-query",
  "slug": "time-query",
  "name": "时间查询 Skill",
  "description": "用于当前时间、时区转换、日期区间和周期统计。",
  "skill_type": "tool",
  "category": "时间类",
  "version": "1.0.0",
  "author": "CompKG-QA",
  "dir_path": "saves/skills/tool/time-query",
  "status": "ready",
  "enabled": false,
  "load_strategy": "lazy",
  "tool_dependencies": [
    "time_query"
  ],
  "mcp_dependencies": [],
  "skill_dependencies": [],
  "scenarios": [
    "通用工具调用",
    "事实校验",
    "辅助计算"
  ],
  "call_example": "把 UTC 时间换算为北京时间并生成近 7 天范围。",
  "params": {
    "top_k": 5,
    "temperature": 0.1,
    "trace": true,
    "timeout_ms": 10000
  }
}
---
# 时间查询 Skill

## 能力说明
用于当前时间、时区转换、日期区间和周期统计。

## 调度规则
- Agent 负责意图识别、选择本 Skill、汇总结果，Skill 负责专门能力执行。
- 仅在问题匹配适用场景时激活，依赖缺失时返回可解释错误。
- 输出必须包含结构化结果、证据/计算过程、依赖状态。

## 输入输出约定
- 输入：用户问题、会话上下文、Agent 传入的 skill_params。
- 输出：answer、evidence、trace、warnings 四类字段。