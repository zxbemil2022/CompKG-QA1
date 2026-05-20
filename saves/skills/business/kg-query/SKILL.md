---
{
  "id": "kg-query",
  "slug": "kg-query",
  "name": "图谱查询 Skill",
  "description": "用于 Neo4j/LightRAG 图谱实体查询、多跳推理与路径解释。",
  "skill_type": "business",
  "category": "图谱类",
  "version": "1.0.0",
  "author": "CompKG-QA",
  "dir_path": "saves/skills/business/kg-query",
  "status": "ready",
  "enabled": true,
  "load_strategy": "session-visible",
  "tool_dependencies": [
    "graph_query",
    "graph_reasoning"
  ],
  "mcp_dependencies": [],
  "skill_dependencies": [
    "math-calculator"
  ],
  "scenarios": [
    "知识库问答",
    "证据引用",
    "408 学科问答"
  ],
  "call_example": "解释 TCP 与可靠传输之间的图谱路径。",
  "params": {
    "top_k": 5,
    "temperature": 0.1,
    "trace": true,
    "timeout_ms": 10000
  }
}
---
# 图谱查询 Skill

## 能力说明
用于 Neo4j/LightRAG 图谱实体查询、多跳推理与路径解释。

## 调度规则
- Agent 负责意图识别、选择本 Skill、汇总结果，Skill 负责专门能力执行。
- 仅在问题匹配适用场景时激活，依赖缺失时返回可解释错误。
- 输出必须包含结构化结果、证据/计算过程、依赖状态。

## 输入输出约定
- 输入：用户问题、会话上下文、Agent 传入的 skill_params。
- 输出：answer、evidence、trace、warnings 四类字段。