from __future__ import annotations

from ..discovery.base import DiscoveryAdapter
from ..governance.policy import evaluate_policy
from ..schemas import CapabilityGraph, ExecutionPlan, IntentSpec, PlanStep


def create_plan(intent: IntentSpec, graph: CapabilityGraph, adapter: DiscoveryAdapter) -> tuple[ExecutionPlan, dict[str, tuple]]:
    steps: list[PlanStep] = []
    discovered: dict[str, tuple] = {}
    unresolved: list[str] = []
    for capability in graph.capabilities:
        candidates = adapter.discover(capability)
        discovered[capability.id] = candidates
        if candidates:
            selected = sorted(candidates, key=lambda c: (-c.claim_confidence, c.id))[0]
            steps.append(PlanStep(
                id=f"step-{len(steps)+1}", capability_id=capability.id, decision="REUSE",
                candidate_id=selected.id, depends_on=capability.depends_on,
                reason=f"best local capability claim ({selected.claim_confidence:.2f}); not capability proof",
            ))
        else:
            unresolved.append(capability.id)
            steps.append(PlanStep(
                id=f"step-{len(steps)+1}", capability_id=capability.id, decision="BUILD",
                candidate_id=None, depends_on=capability.depends_on,
                reason="no candidate returned by the recorded adapter search",
            ))
    governance = evaluate_policy(intent, tuple(unresolved))
    return ExecutionPlan(intent.id, tuple(steps), governance, tuple(unresolved)), discovered

