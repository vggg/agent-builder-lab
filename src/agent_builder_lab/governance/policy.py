from ..schemas import GovernanceDecision, IntentSpec


def evaluate_policy(intent: IntentSpec, unresolved: tuple[str, ...]) -> GovernanceDecision:
    approvals: list[str] = []
    reasons: list[str] = []
    if unresolved:
        reasons.append("unresolved capabilities must be implemented or reviewed")
    if "external_write" in intent.allowed_effects:
        approvals.append("intent-owner")
        reasons.append("external writes require human approval")
    return GovernanceDecision(allowed=not unresolved, required_approvals=tuple(approvals), reasons=tuple(reasons))

