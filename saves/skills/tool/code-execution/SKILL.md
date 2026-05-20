---
{
  "id": "code-execution",
  "slug": "code-execution",
  "name": "代码执行 Skill",
  "description": "用于安全沙箱中的小段代码验证、数据处理和算法演示。",
  "skill_type": "tool",
  "category": "执行类",
  "version": "1.0.0",
  "author": "CompKG-QA",
  "dir_path": "saves/skills/tool/code-execution",
  "status": "sandboxed",
  "enabled": false,
  "load_strategy": "lazy",
  "tool_dependencies": [
    "python_repl"
  ],
  "mcp_dependencies": [],
  "skill_dependencies": [],
  "scenarios": [
    "通用工具调用",
    "事实校验",
    "辅助计算"
  ],
  "call_example": "用 Python 验证排序算法输出是否正确。",
  "params": {
    "top_k": 5,
    "temperature": 0.1,
    "trace": true,
    "timeout_ms": 10000
  }
}
---
# 代码执行 Skill

## 能力说明
用于安全沙箱中的小段代码验证、数据处理和算法演示。

## 调度规则
- Agent 负责意图识别、选择本 Skill、汇总结果，Skill 负责专门能力执行。
- 仅在问题匹配适用场景时激活，依赖缺失时返回可解释错误。
- 输出必须包含结构化结果、证据/计算过程、依赖状态。

## 输入输出约定
- 输入：用户问题、会话上下文、Agent 传入的 skill_params。
- 输出：answer、evidence、trace、warnings 四类字段。