from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import json

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover - deployment requirements normally include PyYAML
    yaml = None

from src import config as sys_config
from src.skills.base import SkillMetadata
from src.utils import logger

_TOOL_DEPENDENCY_ALIASES: dict[str, set[str]] = {
    "web_search": {"tavily_search_results_json", "tavily_search", "TavilySearch"},
    "calculator": {"calculator"},
    "time_query": {"current_time_query"},
    "python_repl": {"python_repl"},
    "graph_query": {"query_knowledge_graph"},
    "graph_reasoning": {"graph_reasoning_visualization"},
    "knowledge_base_search": {"__knowledgebase__", "adaptive_graph_rag_qa"},
    "rerank": {"adaptive_graph_rag_qa"},
    "rule_matcher": {"rule_based_qa"},
    "query": {"query", "execute_query"},
    "execute_modify": {"execute_modify"},
}


class SkillRegistry:
    """文件系统 Skill 注册中心：扫描 SKILL.md、解析依赖、为 Agent 输出运行期工具集合。"""

    def __init__(self, root_dir: Path | None = None):
        self.root_dir = root_dir or Path(sys_config.save_dir) / "skills"
        self._skills: dict[str, SkillMetadata] = {}
        self.reload()

    def reload(self) -> None:
        self._skills = {}
        if not self.root_dir.exists():
            logger.warning(f"Skills root not found: {self.root_dir}")
            return
        for skill_file in sorted(self.root_dir.glob("*/*/SKILL.md")):
            try:
                skill = self._load_skill(skill_file)
                if skill.id:
                    self._skills[skill.id] = skill
            except Exception as exc:  # noqa: BLE001
                logger.warning(f"Failed to load skill metadata from {skill_file}: {exc}")

    def _load_skill(self, skill_file: Path) -> SkillMetadata:
        raw = skill_file.read_text(encoding="utf-8")
        metadata: dict[str, Any] = {}
        body = raw
        if raw.startswith("---"):
            parts = raw.split("---", 2)
            if len(parts) >= 3:
                metadata = (yaml.safe_load(parts[1]) if yaml else json.loads(parts[1])) or {}
                body = parts[2]
        metadata.setdefault("dir_path", str(skill_file.parent))
        return SkillMetadata.from_dict(metadata, base_dir=skill_file.parent, prompt=body)

    def list(self, skill_type: str | None = None) -> list[SkillMetadata]:
        skills = list(self._skills.values())
        if skill_type:
            skills = [skill for skill in skills if skill.skill_type == skill_type]
        return sorted(skills, key=lambda item: (item.skill_type, item.category, item.name))

    def list_dicts(self) -> list[dict[str, Any]]:
        return [skill.to_dict() for skill in self.list()]

    def get(self, skill_id: str) -> SkillMetadata | None:
        return self._skills.get(skill_id)

    def default_enabled_ids(self) -> list[str]:
        return [skill.id for skill in self.list() if skill.enabled]

    def resolve(self, skill_ids: list[str] | None) -> list[SkillMetadata]:
        requested = list(skill_ids or [])
        seen: set[str] = set()
        resolved: list[SkillMetadata] = []

        def visit(skill_id: str) -> None:
            if skill_id in seen:
                return
            seen.add(skill_id)
            skill = self.get(skill_id)
            if not skill:
                logger.warning(f"Unknown skill configured: {skill_id}")
                return
            for dep in skill.skill_dependencies:
                visit(dep)
            resolved.append(skill)

        for skill_id in requested:
            visit(skill_id)
        return resolved

    def build_runtime_prompt(self, skill_ids: list[str] | None, skill_params: dict[str, Any] | None = None) -> str:
        skills = self.resolve(skill_ids)
        if not skills:
            return ""
        skill_params = skill_params or {}
        lines = ["[可用 Skills] Agent 只负责意图识别、选择 Skill、汇总结果；优先调用与问题匹配的 Skill，不要编造。"]
        for skill in skills:
            params = skill_params.get(skill.id, skill.params)
            lines.append(
                f"- {skill.name}({skill.id}, {skill.skill_type}/{skill.category}, v{skill.version}): "
                f"{skill.description}；依赖工具={skill.tool_dependencies or ['无']}；参数={params}；示例={skill.call_example}"
            )
        return "\n".join(lines)

    def dependency_status(self, available_tool_names: set[str], available_mcps: set[str] | None = None) -> dict[str, Any]:
        available_mcps = available_mcps or set()
        result = {}
        for skill in self.list():
            missing_tools = []
            for dep in skill.tool_dependencies:
                aliases = _TOOL_DEPENDENCY_ALIASES.get(dep, {dep})
                if "__knowledgebase__" in aliases:
                    if not any(name.startswith("query_") for name in available_tool_names) and not aliases.intersection(available_tool_names):
                        missing_tools.append(dep)
                elif not aliases.intersection(available_tool_names):
                    missing_tools.append(dep)
            missing_mcps = [dep for dep in skill.mcp_dependencies if dep not in available_mcps]
            result[skill.id] = {
                "ready": not missing_tools and not missing_mcps,
                "missing_tools": missing_tools,
                "missing_mcps": missing_mcps,
            }
        return result

    def filter_tools(self, tools: list[Any], selected_skill_ids: list[str] | None, explicit_tool_ids: list[str] | None = None) -> list[Any]:
        tool_by_name = {getattr(tool, "name", ""): tool for tool in tools}
        selected_names = set(explicit_tool_ids or [])
        include_kb_tools = False
        for skill in self.resolve(selected_skill_ids):
            for dep in skill.tool_dependencies:
                aliases = _TOOL_DEPENDENCY_ALIASES.get(dep, {dep})
                if "__knowledgebase__" in aliases:
                    include_kb_tools = True
                selected_names.update(alias for alias in aliases if alias != "__knowledgebase__")

        if not selected_names and not include_kb_tools:
            return [] if selected_skill_ids == [] or explicit_tool_ids == [] else list(tools)

        enabled = []
        for name, tool in tool_by_name.items():
            metadata = getattr(tool, "metadata", {}) or {}
            tags = metadata.get("tag", []) if isinstance(metadata, dict) else []
            if name in selected_names or (include_kb_tools and (name.startswith("query_") or "knowledgebase" in tags)):
                enabled.append(tool)
        return enabled


@lru_cache(maxsize=1)
def get_skill_registry() -> SkillRegistry:
    return SkillRegistry()
