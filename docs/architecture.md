# Architecture

## Pipeline

```text
IntentSpec
   │ suitability gate
   ▼
CapabilityGraph
   │ one query per capability
   ▼
Discovery adapters ── local / AGNTCY / NANDA / A2A / MCP
   │ normalized AgentCandidate + raw evidence reference
   ▼
Novelty gate ── REUSE / COMPOSE / BUILD / REJECT
   │
   ▼
Governance ── permissions / approvals / limits
   │
   ▼
ExecutionPlan ── executor adapters
   │
   ▼
OutcomeEvidence ── evaluation against IntentSpec
```

The trace observes every boundary and assigns stable event types. Core code never talks directly to a registry or protocol.

## Core schemas

- `IntentSpec`: goal, desired outcome, constraints, allowed effects, evidence requirements, and automation preference.
- `CapabilityGraph`: required capabilities and their dependency edges.
- `AgentCandidate`: normalized discovery claim with source, interface, confidence, and evidence references.
- `ExecutionPlan`: ordered steps, candidate bindings, governance decision, and unresolved gaps.
- `OutcomeEvidence`: an assertion, supporting references, producer, and verification state.

Schemas are Python dataclasses in Milestone 1. JSON Schema or Pydantic may be added only when interchange needs justify another dependency.

## Adapter rule

An adapter translates an external system into the core schemas and retains enough raw evidence to audit that translation. It must not silently upgrade:

```text
claimed capability → verified identity → observed behavior → trusted capability
```

The AGNTCY adapter queries a locally runnable Directory through its AI Catalog/ARD HTTP surface and maps OASF tags plus record metadata. It retains trust-manifest content as an unverified claim. The NANDA adapter should map public discovery/AgentFacts. The A2A adapter should resolve Agent Cards and invoke through an official client. The MCP adapter should enumerate and invoke tools through an MCP client. None of these adapters owns a registry, identity store, trust store, or gateway.

## Novelty gate

For each required capability:

1. reuse an acceptable existing candidate;
2. compose candidates when no single candidate satisfies the requirement;
3. use a conventional API/tool adapter where appropriate;
4. build only for an evidenced gap;
5. reject or require human intervention when risk or uncertainty exceeds policy.

Milestone 1 implements only deterministic `REUSE` and `BUILD`. `COMPOSE` is reserved in the schema, not claimed as working.

## Trust boundaries

Discovery metadata is untrusted input. Selection is not authorization. Planning is not execution. Protocol success is not task success. Task success is not intent satisfaction. The trace must keep these boundaries visible.
