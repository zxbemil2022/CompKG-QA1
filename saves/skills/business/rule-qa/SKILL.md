---
{
  "id": "rule-qa",
  "slug": "rule-qa",
  "name": "规则问答 Skill",
  "description": "用于固定规则、FAQ、评分标准和权限策略类问答。",
  "skill_type": "business",
  "category": "规则类",
  "version": "1.0.0",
  "author": "CompKG-QA",
  "dir_path": "saves/skills/business/rule-qa",
  "status": "ready",
  "enabled": false,
  "load_strategy": "session-visible",
  "tool_dependencies": [
    "rule_matcher"
  ],
  "mcp_dependencies": [],
  "skill_dependencies": [],
  "scenarios": [
    "知识库问答",
    "证据引用",
    "408 学科问答"
  ],
  "call_example": "按规则解释为什么该问答命中低置信度。",
  "params": {
    "top_k": 5,
    "temperature": 0.1,
    "trace": true,
    "timeout_ms": 10000
  }
}
---
# 规则问答 Skill

## 能力说明
用于固定规则、FAQ、评分标准和权限策略类问答。

## 调度规则
- Agent 负责意图识别、选择本 Skill、汇总结果，Skill 负责专门能力执行。
- 仅在问题匹配适用场景时激活，依赖缺失时返回可解释错误。
- 输出必须包含结构化结果、证据/计算过程、依赖状态。

## 输入输出约定
- 输入：用户问题、会话上下文、Agent 传入的 skill_params。
- 输出：answer、evidence、trace、warnings 四类字段。