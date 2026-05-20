from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

SkillType = Literal["tool", "business", "custom"]


@dataclass(slots=True)
class SkillMetadata:
    """标准 Skill 元数据。内容说明保存在 SKILL.md，运行期只依赖这份结构化索引。"""

    id: str
    slug: str
    name: str
    description: str
    skill_type: SkillType
    category: str
    version: str = "1.0.0"
    author: str = "CompKG-QA"
    dir_path: str = ""
    status: str = "ready"
    enabled: bool = False
    load_strategy: str = "lazy"
    tool_dependencies: list[str] = field(default_factory=list)
    mcp_dependencies: list[str] = field(default_factory=list)
    skill_dependencies: list[str] = field(default_factory=list)
    scenarios: list[str] = field(default_factory=list)
    call_example: str = ""
    params: dict[str, Any] = field(default_factory=dict)
    prompt: str = ""
    path: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any], base_dir: Path | None = None, prompt: str = "") -> "SkillMetadata":
        slug = str(data.get("slug") or data.get("id") or "").strip()
        skill_type = str(data.get("skill_type") or data.get("type") or "tool").strip()
        dir_path = str(data.get("dir_path") or (str(base_dir) if base_dir else ""))
        return cls(
            id=str(data.get("id") or slug),
            slug=slug,
            name=str(data.get("name") or slug),
            description=str(data.get("description") or ""),
            skill_type=skill_type if skill_type in {"tool", "business", "custom"} else "tool",
            category=str(data.get("category") or "未分类"),
            version=str(data.get("version") or "1.0.0"),
            author=str(data.get("author") or "CompKG-QA"),
            dir_path=dir_path,
            status=str(data.get("status") or "ready"),
            enabled=bool(data.get("enabled", False)),
            load_strategy=str(data.get("load_strategy") or "lazy"),
            tool_dependencies=list(data.get("tool_dependencies") or []),
            mcp_dependencies=list(data.get("mcp_dependencies") or []),
            skill_dependencies=list(data.get("skill_dependencies") or []),
            scenarios=list(data.get("scenarios") or []),
            call_example=str(data.get("call_example") or ""),
            params=dict(data.get("params") or {}),
            prompt=prompt.strip(),
            path=str(base_dir / "SKILL.md") if base_dir else "",
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "slug": self.slug,
            "name": self.name,
            "description": self.description,
            "skill_type": self.skill_type,
            "category": self.category,
            "version": self.version,
            "author": self.author,
            "dir_path": self.dir_path,
            "status": self.status,
            "enabled": self.enabled,
            "load_strategy": self.load_strategy,
            "tool_dependencies": self.tool_dependencies,
            "mcp_dependencies": self.mcp_dependencies,
            "skill_dependencies": self.skill_dependencies,
            "scenarios": self.scenarios,
            "call_example": self.call_example,
            "params": self.params,
        }
