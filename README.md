# Agent Builder Lab

An open reference implementation and executable lab for a simple question:

> Given a human or business intent, should it be automated with agents—and if so, can existing capabilities be reused or composed before anything new is built?

The lab makes that decision inspectable. It turns an `IntentSpec` into a `CapabilityGraph`, sends every capability through a novelty gate, discovers candidates through adapters, creates a governed `ExecutionPlan`, and records an evidence-bearing trace that can later be evaluated against the original intent.

## What works today

Milestone 1 is deliberately local and deterministic:

```text
intent → suitability decision → capability graph → novelty gate
       → local discovery → governed plan → trace
```

The demo uses a small local catalog. It does **not** call an LLM, execute agents, or claim that capability matching is solved. An opt-in AGNTCY Directory adapter reads the standards-facing AI Catalog/ARD HTTP API; other ecosystem adapters remain explicit stubs.

```bash
python -m agent_builder_lab --scenario scenarios/research.yaml
```

To inspect claims from a local AGNTCY Directory node (adjust its HTTP address as needed):

```bash
python -m agent_builder_lab \
  --scenario scenarios/research.yaml \
  --agntcy-url http://localhost:8080
```

The adapter reads `GET /v1/agents`, maps OASF tags and catalog metadata, and uses exact-tag or transparent lexical matching. Scans are bounded to 100 records and 20 returned candidates by default, and candidates are marked when catalog pagination was truncated; a partial scan is not evidence of global novelty. This is discovery evidence, not verification. Network access is never enabled implicitly.

With an editable install, the equivalent is:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
agentbuilder --scenario scenarios/research.yaml --json trace.json
```

Run the dependency-free tests:

```bash
python -m unittest discover -s tests -v
```

## Example decision

The included research scenario requires `research.web`, `analysis.synthesize`, and `verify.evidence`. The local catalog resolves all three, so the novelty gate chooses `REUSE` three times and the plan requires no new implementation. Changing a capability to an unknown ID produces a `BUILD` decision and blocks execution planning until that gap is addressed.

## Boundaries

This project builds the thin, experimental layer that connects intent to outcomes. It does not recreate:

- agent registries or capability taxonomies;
- identity, reputation, or trust databases;
- protocol gateways or security proxies;
- A2A or MCP clients and servers.

Those belong behind adapters. OASF/AGNTCY, NANDA/NEST, A2A, MCP, and a suitable gateway are inputs to the experiment, not competing implementations.

## Repository map

- `src/agent_builder_lab/intent`: intake and automation-suitability policy
- `src/agent_builder_lab/capabilities`: capability graph construction
- `src/agent_builder_lab/discovery`: adapter contract, local adapter, ecosystem stubs
- `src/agent_builder_lab/planning`: novelty gate and plan construction
- `src/agent_builder_lab/governance`: policy checks and approval boundaries
- `src/agent_builder_lab/execution`: executor contract; execution is intentionally deferred
- `src/agent_builder_lab/evaluation`: outcome/evidence contract
- `src/agent_builder_lab/trace`: append-only research trace
- `docs`: vision, architecture, operating model, and decisions

## Hypotheses under test

1. A stable intermediate capability graph can separate intent reasoning from ecosystem-specific discovery.
2. A reuse-before-build gate can reduce unnecessary agent creation.
3. Claimed capability, verified identity, observed behavior, and trusted capability must remain distinct.
4. Outcome evidence must be tied back to the original intent, not merely to protocol success.

These are hypotheses, not implemented facts. See [the vision](docs/vision.md) and [architecture](docs/architecture.md) for the evidence standard and current status.

## Roadmap

1. **Now — deterministic local:** reproducible intent-to-plan trace.
2. **Now — AGNTCY Directory:** map AI Catalog/ARD records and OASF tags into `AgentCandidate`; retain identity, trust-manifest claims, and match evidence. Next: test against a pinned local container and add structured server-side filtering.
3. **NANDA/NEST:** discover public candidates and capture AgentFacts, availability, and trust unknowns.
4. **A2A:** resolve Agent Cards and invoke selected agents through the official SDK.
5. **MCP:** discover and invoke tools through an MCP client adapter.
6. **Outcome evaluation:** execute a research scenario, validate evidence, and report intent satisfaction separately from task completion.

Contributions should add adapters and experimental results without moving external infrastructure into the core.

## License

Apache-2.0 is suggested and included because this is an interoperability-oriented reference implementation where explicit patent terms are useful. Maintainers should confirm the final license before the first public release.
