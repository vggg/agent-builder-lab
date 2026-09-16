# ADR 0001: Reuse before build

- Status: Accepted
- Date: 2026-09-15

## Context

Agent projects often begin by naming an agent and selecting a framework. That can duplicate existing tools, services, and public agents while hiding the actual business requirement.

## Decision

Every required capability passes through a novelty gate. The default order is reuse, compose, adapt an ordinary service, then build. A build decision must record the searches performed, candidates considered, rejection reasons, and the remaining gap.

Registries, taxonomies, identity systems, trust databases, protocols, and gateways remain external dependencies accessed through adapters.

## Consequences

Plans become more auditable and ecosystem-neutral, and duplicate construction should fall. Discovery quality and metadata mapping become explicit sources of uncertainty. A lack of search results is not proof that no implementation exists, so `BUILD` means “unresolved after the recorded search,” not global novelty.

