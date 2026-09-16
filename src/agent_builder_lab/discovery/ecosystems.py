from __future__ import annotations

from ..schemas import AgentCandidate, Capability
from .base import DiscoveryAdapter


class _NotImplementedAdapter(DiscoveryAdapter):
    def discover(self, capability: Capability) -> tuple[AgentCandidate, ...]:
        raise NotImplementedError(f"{self.name} adapter is a roadmap item; no remote claim was made")


class AgntcyDirectoryAdapter(_NotImplementedAdapter):
    name = "agntcy-directory"


class NandaNestAdapter(_NotImplementedAdapter):
    name = "nanda-nest"


class A2AAdapter(_NotImplementedAdapter):
    name = "a2a"


class MCPAdapter(_NotImplementedAdapter):
    name = "mcp"

