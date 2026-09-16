# Operating model

Agent Builder is a product and governance function, not merely a runtime.

## Intake

An intent owner states the outcome, evidence expectations, constraints, permitted side effects, and acceptable human checkpoints. Intake can result in `do_not_automate`; this is a successful decision, not a pipeline failure.

## Portfolio flow

1. **Qualify:** value, repeatability, ambiguity, reversibility, data sensitivity, and consequences.
2. **Model:** produce and review the capability graph.
3. **Research:** run the novelty gate and retain rejected candidates and reasons.
4. **Design:** choose reuse, composition, ordinary automation, or a new implementation.
5. **Govern:** set permissions, approvals, monitoring, budgets, and rollback behavior.
6. **Operate:** observe quality, cost, incidents, overrides, and reuse.
7. **Evaluate:** measure business outcome against the original intent; retire or revise weak solutions.

## Decision rights

- The intent owner accepts the outcome definition.
- The Agent Builder function owns intake quality, patterns, portfolio visibility, and design review.
- Security/data owners approve permissions and sensitive-data boundaries.
- Capability owners attest interfaces and operational expectations.
- A human approver owns irreversible or high-impact actions.

## Quality gates

A project advances only when its intent is testable, the novelty search is recorded, candidate claims are distinguished from verified evidence, permissions are least-privilege, failure/rollback behavior is defined, and outcome metrics exist.

## Measures

Track intent satisfaction, evidence coverage, unsupported claims, human overrides, incidents, latency/cost, reuse rate, capabilities built despite existing alternatives, and time from intake to validated outcome. Avoid treating number of agents as success.

