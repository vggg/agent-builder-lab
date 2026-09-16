from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal


@dataclass(frozen=True)
class IntentSpec:
    id: str
    goal: str
    desired_outcome: str
    constraints: tuple[str, ...] = ()
    allowed_effects: tuple[str, ...] = ("read_local",)
    evidence_required: bool = True
    automation_preference: Literal["assist", "automate", "unspecified"] = "unspecified"


@dataclass(frozen=True)
class Capability:
    id: str
    description: str
    depends_on: tuple[str, ...] = ()


@dataclass(frozen=True)
class CapabilityGraph:
    intent_id: str
    capabilities: tuple[Capability, ...]


@dataclass(frozen=True)
class AgentCandidate:
    id: str
    name: str
    capabilities: tuple[str, ...]
    source: str
    interface: str
    endpoint: str | None = None
    claim_confidence: float = 0.0
    evidence_refs: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PlanStep:
    id: str
    capability_id: str
    decision: Literal["REUSE", "COMPOSE", "BUILD", "REJECT"]
    candidate_id: str | None
    depends_on: tuple[str, ...] = ()
    reason: str = ""


@dataclass(frozen=True)
class GovernanceDecision:
    allowed: bool
    required_approvals: tuple[str, ...] = ()
    reasons: tuple[str, ...] = ()


@dataclass(frozen=True)
class ExecutionPlan:
    intent_id: str
    steps: tuple[PlanStep, ...]
    governance: GovernanceDecision
    unresolved_capabilities: tuple[str, ...] = ()


@dataclass(frozen=True)
class OutcomeEvidence:
    intent_id: str
    assertion: str
    producer: str
    references: tuple[str, ...] = ()
    verification: Literal["unverified", "verified", "disputed"] = "unverified"


def to_dict(value: Any) -> dict[str, Any]:
    return asdict(value)
