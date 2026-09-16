from __future__ import annotations

from typing import Any

from ..schemas import AgentCandidate, Capability
from .base import DiscoveryAdapter


class LocalDiscoveryAdapter(DiscoveryAdapter):
    name = "local"

    def __init__(self, records: list[dict[str, Any]]) -> None:
        self._records = records

    def discover(self, capability: Capability) -> tuple[AgentCandidate, ...]:
        return tuple(AgentCandidate(
            id=r["id"], name=r["name"], capabilities=tuple(r["capabilities"]),
            source=self.name, interface=r.get("interface", "python"),
            endpoint=r.get("endpoint"), claim_confidence=float(r.get("claim_confidence", 0.5)),
            evidence_refs=tuple(r.get("evidence_refs", [])),
        ) for r in self._records if capability.id in r["capabilities"])

