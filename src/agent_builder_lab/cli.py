from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from .capabilities import build_graph
from .discovery import LocalDiscoveryAdapter
from .intent import assess_suitability, resolve_intent
from .planning import create_plan
from .trace import Trace


def run_scenario(path: Path) -> Trace:
    data = json.loads(path.read_text(encoding="utf-8"))
    trace = Trace()
    intent = resolve_intent(data["intent"])
    trace.record("intent.resolved", asdict(intent))
    suitable, reasons = assess_suitability(intent)
    trace.record("intent.suitability", {"suitable": suitable, "reasons": reasons})
    if not suitable:
        return trace
    graph = build_graph(intent, data["capabilities"])
    trace.record("capabilities.graph_created", asdict(graph))
    plan, discovered = create_plan(intent, graph, LocalDiscoveryAdapter(data["local_catalog"]))
    trace.record("discovery.completed", {
        capability: [asdict(candidate) for candidate in candidates]
        for capability, candidates in discovered.items()
    })
    trace.record("novelty_gate.decided", {
        step.capability_id: {"decision": step.decision, "reason": step.reason}
        for step in plan.steps
    })
    trace.record("plan.created", asdict(plan))
    return trace


def _print_trace(trace: Trace) -> None:
    print("AGENT BUILDER LAB — deterministic planning trace")
    for event in trace.events:
        print(f"\n{event.sequence}. {event.kind.upper()}")
        if event.kind == "novelty_gate.decided":
            for capability, decision in event.data.items():
                print(f"   {capability}: {decision['decision']} — {decision['reason']}")
        elif event.kind == "plan.created":
            print(f"   governance allowed: {event.data['governance']['allowed']}")
            print(f"   unresolved: {event.data['unresolved_capabilities'] or 'none'}")
        else:
            print(f"   {json.dumps(event.data, sort_keys=True)}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Turn intent into an inspectable, governed agent plan")
    parser.add_argument("--scenario", type=Path, required=True, help="JSON-compatible YAML scenario")
    parser.add_argument("--json", type=Path, help="optional trace output path")
    args = parser.parse_args(argv)
    trace = run_scenario(args.scenario)
    _print_trace(trace)
    if args.json:
        args.json.write_text(json.dumps(trace.as_dict(), indent=2) + "\n", encoding="utf-8")
    return 0

