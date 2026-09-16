from __future__ import annotations

from typing import Any

from ..schemas import Capability, CapabilityGraph, IntentSpec


def build_graph(intent: IntentSpec, items: list[dict[str, Any]]) -> CapabilityGraph:
    capabilities = tuple(Capability(
        id=item["id"], description=item["description"],
        depends_on=tuple(item.get("depends_on", [])),
    ) for item in items)
    known = {cap.id for cap in capabilities}
    missing = {dep for cap in capabilities for dep in cap.depends_on if dep not in known}
    if missing:
        raise ValueError(f"unknown capability dependencies: {sorted(missing)}")
    return CapabilityGraph(intent_id=intent.id, capabilities=capabilities)

