from __future__ import annotations

from abc import ABC, abstractmethod

from ..schemas import AgentCandidate, Capability


class DiscoveryAdapter(ABC):
    name: str

    @abstractmethod
    def discover(self, capability: Capability) -> tuple[AgentCandidate, ...]:
        """Return normalized claims; do not imply verification or trust."""

