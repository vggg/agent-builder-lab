from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class TraceEvent:
    sequence: int
    kind: str
    timestamp: str
    data: dict[str, Any]


class Trace:
    def __init__(self) -> None:
        self.events: list[TraceEvent] = []

    def record(self, kind: str, data: dict[str, Any]) -> None:
        self.events.append(TraceEvent(
            sequence=len(self.events) + 1, kind=kind,
            timestamp=datetime.now(timezone.utc).isoformat(), data=data,
        ))

    def as_dict(self) -> dict[str, Any]:
        return {"schema_version": "0.1", "events": [asdict(event) for event in self.events]}

