from __future__ import annotations

import json
from pathlib import Path


def load_repo_graph(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def node_ids(graph: dict) -> set[str]:
    return {node["id"] for node in graph["nodes"]}


def validate_edges(graph: dict) -> bool:
    ids = node_ids(graph)
    return all(edge[0] in ids and edge[1] in ids and len(edge) == 3 for edge in graph["edges"])


def adjacency(graph: dict) -> dict[str, list[str]]:
    adj = {node: [] for node in node_ids(graph)}
    for source, target, _ in graph["edges"]:
        adj[source].append(target)
    return adj
