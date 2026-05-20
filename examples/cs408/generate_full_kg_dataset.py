"""Generate CS408 KG dataset with semantic-first deterministic construction.

Design goals:
1) Avoid synthetic template names like `学科-章节-类型NN`
2) Avoid random relation sampling that weakens semantics
3) Build from expert seed + curated chapter taxonomy
"""

from __future__ import annotations

import csv
import json
from pathlib import Path


ALLOWED_RELATIONS = {
    "BELONGS_TO",
    "HAS_SUB",
    "HAS_METHOD",
    "HAS_PROPERTY",
    "HAS_COMPLEXITY",
    "PREREQUISITE",
    "CAUSE",
    "USED_IN",
    "EQUIVALENT",
    "DEPENDS_ON",
    "OPTIMIZED_BY",
    "SOLVES",
    "VERIFIED_BY",
    "MEASURED_BY",
    "APPLIES_TO",
}

RELATION_WEIGHT = {
    "BELONGS_TO": 1.0,
    "HAS_SUB": 0.95,
    "HAS_METHOD": 0.92,
    "HAS_PROPERTY": 0.9,
    "HAS_COMPLEXITY": 0.9,
    "PREREQUISITE": 0.88,
    "CAUSE": 0.85,
    "USED_IN": 0.84,
    "EQUIVALENT": 0.82,
    "DEPENDS_ON": 0.8,
    "OPTIMIZED_BY": 0.8,
    "SOLVES": 0.83,
    "VERIFIED_BY": 0.78,
    "MEASURED_BY": 0.78,
    "APPLIES_TO": 0.79,
}
CHAPTER_TAXONOMY: dict[str, dict[str, dict[str, list[str]]]] = {
    "数据结构": {
        "线性表": {
            "Concept": ["顺序表", "链表", "栈", "队列", "循环队列"],
            "Method": ["头插法", "尾插法", "顺序遍历"],
            "Property": ["先进先出", "后进先出"],
        },
        "树与图": {
            "Concept": ["二叉树", "平衡二叉树", "红黑树", "图", "最小生成树", "最短路径"],
            "Method": ["深度优先搜索", "广度优先搜索", "Prim算法", "Kruskal算法", "Dijkstra算法"],
            "Property": ["连通性", "无环性"],
        },
        "查找排序": {
            "Concept": ["哈希表", "快速排序", "归并排序", "堆排序"],
            "Method": ["分治", "堆调整", "散列函数设计"],
            "Property": ["稳定性", "时间复杂度"],
        },
    },
    "操作系统": {
        "进程线程": {
            "Concept": ["进程", "线程", "进程同步", "进程调度", "死锁"],
            "Method": ["互斥锁", "信号量", "银行家算法"],
            "Property": ["上下文切换开销", "并发性"],
        },
        "内存管理": {
            "Concept": ["虚拟内存", "页表", "页面置换", "内存保护"],
            "Method": ["LRU", "FIFO", "时钟算法"],
            "Property": ["局部性原理", "缺页率"],
        },
        "文件系统": {
            "Concept": ["文件系统", "目录结构", "磁盘调度", "inode"],
            "Method": ["索引分配", "SCAN", "SSTF"],
            "Property": ["一致性", "持久性"],
        },
    },
    "计算机网络": {
        "应用层": {
            "Concept": ["HTTP", "DNS", "SMTP", "FTP"],
            "Method": ["域名解析", "请求响应模型"],
            "Property": ["无状态协议", "应用层语义"],
        },
        "传输层": {
            "Concept": ["TCP", "UDP", "拥塞控制", "流量控制"],
            "Method": ["三次握手", "四次挥手", "滑动窗口", "慢启动"],
            "Property": ["可靠传输", "面向连接"],
        },
        "网络层": {
            "Concept": ["IP", "IPv4", "IPv6", "路由选择"],
            "Method": ["RIP", "OSPF", "CIDR"],
            "Property": ["分片", "寻址"],
        },
    },
    "计算机组成原理": {
        "数据表示": {
            "Concept": ["补码", "浮点数", "IEEE754", "字长"],
            "Method": ["规格化", "舍入策略"],
            "Property": ["表示范围", "精度"],
        },
        "指令系统": {
            "Concept": ["指令周期", "寻址方式", "控制器", "微程序"],
            "Method": ["取指", "译码", "执行"],
            "Property": ["指令并行性", "指令兼容性"],
        },
        "存储系统": {
            "Concept": ["Cache", "主存", "总线", "DMA"],
            "Method": ["写回策略", "写直达策略", "预取"],
            "Property": ["命中率", "带宽"],
        },
        "流水线": {
            "Concept": ["流水线冲突", "结构相关", "数据相关", "控制相关"],
            "Method": ["旁路转发", "分支预测", "暂停气泡"],
            "Property": ["吞吐率", "加速比"],
        },
    },
}



def load_expert_seed(path: Path) -> list[dict]:
    triples = []
    if not path.exists():
        return triples
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            rel = str(row.get("r", "")).strip().upper()
            if rel not in ALLOWED_RELATIONS:
                continue
            triples.append(
                {
                    "h": str(row.get("h", "")).strip(),
                    "h_type": str(row.get("h_type", "Concept")).strip(),
                    "r": rel,
                    "t": str(row.get("t", "")).strip(),
                    "t_type": str(row.get("t_type", "Concept")).strip(),
                    "subject": str(row.get("subject", "")).strip(),
                }
            )
    return triples


def build_curated_taxonomy_triples() -> list[dict]:
    triples: list[dict] = []
    for subject, chapters in CHAPTER_TAXONOMY.items():
        for chapter, groups in chapters.items():
            triples.append(
                {
                    "h": chapter,
                    "h_type": "Chapter",
                    "r": "BELONGS_TO",
                    "t": subject,
                    "t_type": "Course",
                    "subject": subject,
                }
            )
            for entity_type, terms in groups.items():
                for term in terms:
                    triples.append(
                        {
                            "h": chapter,
                            "h_type": "Chapter",
                            "r": "HAS_SUB",
                            "t": term,
                            "t_type": entity_type,
                            "subject": subject,
                        }
                    )
    return triples


def expand_cs408_knowledge_points(triples: list[dict]) -> list[dict]:
    """按 408 教学语义扩展知识点（避免无意义随机名称）。"""
    expanded: list[dict] = []

    concept_terms = {
        t["t"]
        for t in triples
        if t.get("t_type") in {"Concept", "Method"} and t.get("t")
    }
    chapter_subject = {
        t["h"]: t["subject"]
        for t in triples
        if t.get("h_type") == "Chapter" and t.get("subject")
    }

    for term in sorted(concept_terms):
        subject = next(
            (t.get("subject", "") for t in triples if t.get("t") == term and t.get("subject")),
            "",
        )
        subject = subject or "综合"
        expanded.extend(
            [
                {
                    "h": term,
                    "h_type": "Concept",
                    "r": "HAS_PROPERTY",
                    "t": f"{term}核心定义",
                    "t_type": "Property",
                    "subject": subject,
                },
                {
                    "h": term,
                    "h_type": "Concept",
                    "r": "HAS_PROPERTY",
                    "t": f"{term}判定条件",
                    "t_type": "Property",
                    "subject": subject,
                },
                {
                    "h": term,
                    "h_type": "Concept",
                    "r": "USED_IN",
                    "t": f"{term}考研真题场景",
                    "t_type": "Example",
                    "subject": subject,
                },
                {
                    "h": f"{term}考研真题场景",
                    "h_type": "Example",
                    "r": "VERIFIED_BY",
                    "t": f"{term}典型题型",
                    "t_type": "Example",
                    "subject": subject,
                },
                {
                    "h": term,
                    "h_type": "Concept",
                    "r": "MEASURED_BY",
                    "t": f"{term}高频考点权重",
                    "t_type": "Property",
                    "subject": subject,
                },
                {
                    "h": term,
                    "h_type": "Concept",
                    "r": "HAS_PROPERTY",
                    "t": f"{term}易错陷阱",
                    "t_type": "Property",
                    "subject": subject,
                },
                {
                    "h": term,
                    "h_type": "Concept",
                    "r": "APPLIES_TO",
                    "t": f"{term}应用边界",
                    "t_type": "Property",
                    "subject": subject,
                },
                {
                    "h": term,
                    "h_type": "Concept",
                    "r": "OPTIMIZED_BY",
                    "t": f"{term}优化策略",
                    "t_type": "Method",
                    "subject": subject,
                },
            ]
        )

    # 每章补充考点导航节点，增强图谱可解释与路径推荐能力
    for chapter, subject in sorted(chapter_subject.items()):
        expanded.extend(
            [
                {
                    "h": chapter,
                    "h_type": "Chapter",
                    "r": "HAS_SUB",
                    "t": f"{chapter}高频考点清单",
                    "t_type": "Concept",
                    "subject": subject,
                },
                {
                    "h": f"{chapter}高频考点清单",
                    "h_type": "Concept",
                    "r": "HAS_METHOD",
                    "t": f"{chapter}高效复习策略",
                    "t_type": "Method",
                    "subject": subject,
                },
                {
                    "h": f"{chapter}高效复习策略",
                    "h_type": "Method",
                    "r": "APPLIES_TO",
                    "t": f"{chapter}常见失分点",
                    "t_type": "Property",
                    "subject": subject,
                },
            ]
        )

    return triples + expanded


def dedupe_triples(triples: list[dict]) -> list[dict]:
    unique: dict[tuple[str, str, str, str], dict] = {}
    for t in triples:
        key = (t["h"], t["r"], t["t"], t["subject"])
        unique[key] = t
    return list(unique.values())


def triples_to_nodes_edges(triples: list[dict]) -> tuple[list[dict], list[dict]]:
    node_type_map: dict[str, str] = {}
    node_subject_map: dict[str, set[str]] = {}
    chapter_hint: dict[str, str] = {}

    for t in triples:
        for node_key, type_key in [("h", "h_type"), ("t", "t_type")]:
            node_name = t[node_key]
            node_type_map[node_name] = t[type_key]
            node_subject_map.setdefault(node_name, set()).update(
                [s for s in str(t.get("subject", "")).split("|") if s]
            )
        if t["h_type"] == "Chapter":
            chapter_hint[t["h"]] = t["h"]
        elif t["r"] == "HAS_SUB" and t["h_type"] == "Chapter":
            chapter_hint[t["t"]] = t["h"]

    node_names = sorted(node_type_map.keys())
    node_id_map = {name: f"N{i + 1:05d}" for i, name in enumerate(node_names)}
    nodes = []
    for name in node_names:
        subjects = sorted(node_subject_map.get(name, set()))
        nodes.append(
            {
                "id": node_id_map[name],
                "name": name,
                "subject": "|".join(subjects),
                "chapter": chapter_hint.get(name, ""),
                "type": node_type_map[name],
            }
        )

    edges = []
    for t in triples:
        relation = t["r"]
        edges.append(
             {
                "source": node_id_map[t["h"]],
                "target": node_id_map[t["t"]],
                "relation": relation,
                "subject": t["subject"],
                "weight": RELATION_WEIGHT.get(relation, 0.75),
            }
        )
        return nodes, edges


def main() -> None:
    base = Path(__file__).resolve().parent
    expert_seed = load_expert_seed(base / "cs408_expert_seed.jsonl")
    curated = build_curated_taxonomy_triples()
    triples = dedupe_triples(expand_cs408_knowledge_points(expert_seed + curated))
    nodes, edges = triples_to_nodes_edges(triples)

    (base / "cs408_full_kg_nodes.json").write_text(json.dumps(nodes, ensure_ascii=False, indent=2), encoding="utf-8")
    with (base / "cs408_full_kg_edges.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["source", "target", "relation", "subject", "weight"])
        writer.writeheader()
        writer.writerows(edges)

    (base / "cs408_full_kg_triples.json").write_text(json.dumps(triples, ensure_ascii=False, indent=2), encoding="utf-8")
    with (base / "cs408_full_kg_triples.jsonl").open("w", encoding="utf-8") as f:
        for t in triples:
            f.write(json.dumps(t, ensure_ascii=False) + "\n")

    meta = {
        "generation_mode": "semantic_curated",
        "node_count": len(nodes),
        "edge_count": len(edges),
        "subject_count": len(CHAPTER_TAXONOMY),
        "subjects": sorted(CHAPTER_TAXONOMY.keys()),
        "allowed_relations": sorted(list(ALLOWED_RELATIONS)),
    }
    (base / "cs408_full_kg_meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(meta)


if __name__ == "__main__":
    main()


