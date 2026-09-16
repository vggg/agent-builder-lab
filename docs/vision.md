# Vision

## Mission

Given a business or human intent, determine whether agentic automation is appropriate, identify the capabilities required, reuse existing agents and tools where possible, compose or build only what is missing, execute under explicit governance, and evaluate whether the original intent was satisfied.

The public artifact is an executable research lab: code, architecture, and experiment traces live together. A failed experiment that exposes a semantic or trust gap is useful output.

## Questions

- Can intent be converted into a portable capability graph?
- Can that graph resolve consistently against OASF/AGNTCY, NANDA/NEST, A2A, and MCP descriptions?
- Can candidate selection distinguish claims from evidence?
- Can permissions and human approval be scoped to the originating intent?
- Can outcome satisfaction be assessed independently of transport success?

## Principles

1. Start with the outcome, not an agent.
2. Decide whether automation is appropriate before decomposition.
3. Search before building; compose before specializing.
4. Put ecosystem-specific behavior behind adapters.
5. Preserve raw inputs, transformations, decisions, and uncertainty.
6. Treat human review, rollback, and refusal as valid plan outcomes.

## Facts versus hypotheses

**Implemented facts in Milestone 1:** typed schemas exist; a deterministic scenario is parsed; rules create a capability graph; a local adapter returns candidates; the novelty gate emits reuse/build decisions; policy checks produce a plan; an ordered trace records those stages.

**Not yet implemented:** semantic decomposition, OASF mapping, remote discovery, identity verification, trust scoring, A2A/MCP invocation, rollback, and outcome evaluation over real work.

**Hypotheses:** the capability graph is a useful intermediate representation; reuse-first decisions remain explainable at scale; adapter-normalized metadata is sufficient for defensible planning; evidence can travel through execution strongly enough to evaluate the initiating intent.

Every experiment should label observations, inferences, and hypotheses separately. Self-declared metadata is an observation about a claim, not proof of capability.

## Success

Minimum success is a reproducible trace from intent to governed plan. Strong success is discovery and composition of previously unknown public capabilities through standard protocols. Exceptional success is repeatable intent satisfaction across domains without target-specific orchestration code.

