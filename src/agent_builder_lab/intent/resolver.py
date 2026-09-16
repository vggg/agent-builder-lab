from __future__ import annotations

from typing import Any

from ..schemas import IntentSpec


def resolve_intent(data: dict[str, Any]) -> IntentSpec:
    return IntentSpec(
        id=data["id"], goal=data["goal"], desired_outcome=data["desired_outcome"],
        constraints=tuple(data.get("constraints", [])),
        allowed_effects=tuple(data.get("allowed_effects", ["read_local"])),
        evidence_required=bool(data.get("evidence_required", True)),
        automation_preference=data.get("automation_preference", "unspecified"),
    )


def assess_suitability(intent: IntentSpec) -> tuple[bool, tuple[str, ...]]:
    reasons: list[str] = []
    if not intent.goal.strip() or not intent.desired_outcome.strip():
        reasons.append("goal and desired outcome must be explicit")
    risky = {"financial_transaction", "physical_control", "irreversible_external_write"}
    if risky.intersection(intent.allowed_effects):
        reasons.append("high-impact effects require human-led design review")
    return (not reasons, tuple(reasons))

