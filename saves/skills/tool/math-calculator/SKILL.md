---
{
  "id": "math-calculator",
  "slug": "math-calculator",
  "name": "数学计算 Skill",
  "description": "用于公式计算、复杂度估算、统计指标计算和数值校验。",
  "skill_type": "tool",
  "category": "计算类",
  "version": "1.0.0",
  "author": "CompKG-QA",
  "dir_path": "saves/skills/tool/math-calculator",
  "status": "ready",
  "enabled": true,
  "load_strategy": "preload",
  "tool_dependencies": [
    "calculator"
  ],
  "mcp_dependencies": [],
  "skill_dependencies": [],
  "scenarios": [
    "通用工具调用",
    "事实校验",
    "辅助计算"
  ],
  "call_example": "计算哈希查找平均时间复杂度相关指标。",
  "params": {
    "top_k": 5,
    "temperature": 0,
    "trace": true,
    "timeout_ms": 10000
  }
}
---
# 数学计算 Skill

## 能力说明
用于公式计算、复杂度估算、统计指标计算和数值校验。

## 调度规则
- Agent 负责意图识别、选择本 Skill、汇总结果，Skill 负责专门能力执行。
- 仅在问题匹配适用场景时激活，依赖缺失时返回可解释错误。
- 输出必须包含结构化结果、证据/计算过程、依赖状态。

## 输入输出约定
- 输入：用户问题、会话上下文、Agent 传入的 skill_params。
- 输出：answer、evidence、trace、warnings 四类字段。