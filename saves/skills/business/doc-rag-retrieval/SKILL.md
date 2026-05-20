---
{
  "id": "doc-rag-retrieval",
  "slug": "doc-rag-retrieval",
  "name": "文档检索 Skill",
  "description": "用于向量库 RAG 精准检索、证据重排与答案引用。",
  "skill_type": "business",
  "category": "检索类",
  "version": "1.0.0",
  "author": "CompKG-QA",
  "dir_path": "saves/skills/business/doc-rag-retrieval",
  "status": "ready",
  "enabled": true,
  "load_strategy": "session-visible",
  "tool_dependencies": [
    "knowledge_base_search",
    "rerank"
  ],
  "mcp_dependencies": [],
  "skill_dependencies": [],
  "scenarios": [
    "知识库问答",
    "证据引用",
    "408 学科问答"
  ],
  "call_example": "从知识库检索 OS 死锁条件并附来源。",
  "params": {
    "top_k": 5,
    "temperature": 0.1,
    "trace": true,
    "timeout_ms": 10000
  }
}
---
# 文档检索 Skill

## 能力说明
用于向量库 RAG 精准检索、证据重排与答案引用。

## 调度规则
- Agent 负责意图识别、选择本 Skill、汇总结果，Skill 负责专门能力执行。
- 仅在问题匹配适用场景时激活，依赖缺失时返回可解释错误。
- 输出必须包含结构化结果、证据/计算过程、依赖状态。

## 输入输出约定
- 输入：用户问题、会话上下文、Agent 传入的 skill_params。
- 输出：answer、evidence、trace、warnings 四类字段。