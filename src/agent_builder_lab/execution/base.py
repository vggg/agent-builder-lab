from __future__ import annotations

from abc import ABC, abstractmethod

from ..schemas import ExecutionPlan, OutcomeEvidence


class Executor(ABC):
    @abstractmethod
    def execute(self, plan: ExecutionPlan) -> tuple[OutcomeEvidence, ...]:
        """Execute an approved plan. Milestone 1 provides no concrete executor."""

