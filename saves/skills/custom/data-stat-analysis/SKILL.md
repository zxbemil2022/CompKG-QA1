---
{
  "id": "data-stat-analysis",
  "slug": "data-stat-analysis",
  "name": "数据统计与分析 Skill",
  "description": "用于会话统计、趋势洞察、异常数据诊断和指标解释。",
  "skill_type": "custom",
  "category": "数据分析",
  "version": "1.0.0",
  "author": "CompKG-QA",
  "dir_path": "saves/skills/custom/data-stat-analysis",
  "status": "ready",
  "enabled": true,
  "load_strategy": "triggered",
  "tool_dependencies": [
    "calculator"
  ],
  "mcp_dependencies": [],
  "skill_dependencies": [
    "math-calculator"
  ],
  "scenarios": [
    "组合业务场景",
    "管理分析",
    "结果交付"
  ],
  "call_example": "分析最近 7 天问答活跃度下降原因。",
  "params": {
    "top_k": 5,
    "temperature": 0,
    "trace": true,
    "timeout_ms": 10000
  }
}
---
# 数据统计与分析 Skill

## 能力说明
用于会话统计、趋势洞察、异常数据诊断和指标解释。

## 调度规则
- Agent 负责意图识别、选择本 Skill、汇总结果，Skill 负责专门能力执行。
- 仅在问题匹配适用场景时激活，依赖缺失时返回可解释错误。
- 输出必须包含结构化结果、证据/计算过程、依赖状态。

## 输入输出约定
- 输入：用户问题、会话上下文、Agent 传入的 skill_params。
- 输出：answer、evidence、trace、warnings 四类字段。