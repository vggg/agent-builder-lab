from pathlib import Path
import unittest

from agent_builder_lab.cli import run_scenario
from agent_builder_lab.capabilities import build_graph
from agent_builder_lab.discovery import LocalDiscoveryAdapter
from agent_builder_lab.intent import resolve_intent
from agent_builder_lab.planning import create_plan


ROOT = Path(__file__).parents[1]


class PipelineTests(unittest.TestCase):
    def test_research_scenario_reuses_every_capability(self) -> None:
        trace = run_scenario(ROOT / "scenarios/research.yaml")
        plan = trace.events[-1].data
        self.assertTrue(plan["governance"]["allowed"])
        self.assertEqual((), plan["unresolved_capabilities"])
        novelty = trace.events[-2].data
        self.assertEqual({"REUSE"}, {item["decision"] for item in novelty.values()})

    def test_missing_candidate_becomes_build_gap(self) -> None:
        intent = resolve_intent({"id": "i", "goal": "g", "desired_outcome": "o"})
        graph = build_graph(intent, [{"id": "missing", "description": "not in catalog"}])
        plan, _ = create_plan(intent, graph, LocalDiscoveryAdapter([]))
        self.assertEqual("BUILD", plan.steps[0].decision)
        self.assertFalse(plan.governance.allowed)
        self.assertEqual(("missing",), plan.unresolved_capabilities)

    def test_unknown_dependency_is_rejected(self) -> None:
        intent = resolve_intent({"id": "i", "goal": "g", "desired_outcome": "o"})
        with self.assertRaises(ValueError):
            build_graph(intent, [{"id": "a", "description": "a", "depends_on": ["b"]}])

    def test_weak_claim_remains_visible_but_does_not_pass_novelty_gate(self) -> None:
        intent = resolve_intent({"id": "i", "goal": "g", "desired_outcome": "o"})
        graph = build_graph(intent, [{"id": "weak", "description": "weak"}])
        catalog = [{
            "id": "candidate", "name": "Weak claim", "capabilities": ["weak"],
            "claim_confidence": 0.40,
        }]
        plan, discovered = create_plan(intent, graph, LocalDiscoveryAdapter(catalog))
        self.assertEqual(1, len(discovered["weak"]))
        self.assertEqual("BUILD", plan.steps[0].decision)
        self.assertIn("threshold", plan.steps[0].reason)


if __name__ == "__main__":
    unittest.main()
