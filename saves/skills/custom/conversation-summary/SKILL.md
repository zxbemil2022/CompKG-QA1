---
{
  "id": "conversation-summary",
  "slug": "conversation-summary",
  "name": "多轮对话梳理 Skill",
  "description": "用于多轮上下文压缩、意图追踪、待办总结与问答归档。",
  "skill_type": "custom",
  "category": "对话治理",
  "version": "1.0.0",
  "author": "CompKG-QA",
  "dir_path": "saves/skills/custom/conversation-summary",
  "status": "ready",
  "enabled": true,
  "load_strategy": "triggered",
  "tool_dependencies": [],
  "mcp_dependencies": [],
  "skill_dependencies": [
    "doc-rag-retrieval"
  ],
  "scenarios": [
    "组合业务场景",
    "管理分析",
    "结果交付"
  ],
  "call_example": "总结本轮对话中用户最终确认的问题和结论。",
  "params": {
    "top_k": 5,
    "temperature": 0.1,
    "trace": true,
    "timeout_ms": 10000
  }
}
---
# 多轮对话梳理 Skill

## 能力说明
用于多轮上下文压缩、意图追踪、待办总结与问答归档。

## 调度规则
- Agent 负责意图识别、选择本 Skill、汇总结果，Skill 负责专门能力执行。
- 仅在问题匹配适用场景时激活，依赖缺失时返回可解释错误。
- 输出必须包含结构化结果、证据/计算过程、依赖状态。

## 输入输出约定
- 输入：用户问题、会话上下文、Agent 传入的 skill_params。
- 输出：answer、evidence、trace、warnings 四类字段。