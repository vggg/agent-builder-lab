from ..schemas import IntentSpec, OutcomeEvidence


def evaluate_outcome(intent: IntentSpec, evidence: tuple[OutcomeEvidence, ...]) -> tuple[bool, str]:
    if not evidence:
        return False, "no outcome evidence was produced"
    if intent.evidence_required and not any(item.verification == "verified" for item in evidence):
        return False, "the intent requires evidence but none is verified"
    return True, "minimum evidence policy satisfied; semantic intent evaluation remains a hypothesis"

