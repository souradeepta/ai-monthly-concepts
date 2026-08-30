# Model routing
Status: durable
Sources: [Google Cloud — Model selection](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/models)
## In one sentence
Model routing selects a model or fallback using task quality, risk, modality, latency, and cost requirements.
## Background: what existed before
Teams commonly hard-coded one model per product. Model diversity and variable traffic now make selection a runtime systems decision.
## What changed and why now
Specialized, small, and large models create a quality-cost frontier; routers can classify requests and choose an appropriate tier.
## Impact on current processing and architecture
A router needs policy, health checks, deadlines, budgets, and consistent output contracts. Route logs are essential for debugging drift.
## Real-world applications and constraints
Extraction can use a small model while ambiguous or high-risk work escalates. Fallbacks may change behavior and must preserve privacy and schema.
## Mental model
```mermaid
flowchart LR
 Q[Request]-->R[Risk/task router]-->S[Small model]
 R-->L[Large model]; S-->V[Validator]; L-->V
 classDef a fill:#dbeafe,stroke:#2563eb,color:#172554
 classDef b fill:#fef3c7,stroke:#d97706,color:#451a03
 classDef c fill:#dcfce7,stroke:#16a34a,color:#14532d
 class Q a; class R,S,L b; class V c
```
```mermaid
sequenceDiagram
 participant C as Client
 participant R as Router
 participant M as Model
 C->>R: request + deadline
 R->>M: selected model
 M-->>R: result
 alt timeout or invalid schema
  R->>M: fallback model
 end
 R-->>C: validated result + route metadata
```
## What changed this month
The March map frames routing as an operational trade-off rather than a leaderboard choice.
## Engineering consequence
Define routing thresholds and fallback contracts; compare per-route quality, p95, and spend.
## Limits and failure modes
Misclassification sends risky work to weak models; fallback can duplicate cost or expose data to an unintended provider.
## Runnable low-cost example
```python
def route(risk, tokens): return "large" if risk == "high" or tokens > 500 else "small"
print(route("low", 40), route("high", 40))
```
## Mini exercise (15–30 min)
Add a deadline and route unavailable models to a deterministic template.
## Build it locally
1. Run `python3 router.py`.
2. Define low/high-risk fixtures.
3. Add model health and schema checks.
4. Record route, latency, and cost estimates.
## Interview Q&A
**What inputs matter?** Risk, task type, context size, deadline, and budget. **Why fallback?** Availability and latency. **What must remain stable?** Authorization and output contract.
## Glossary
**Router:** runtime model selector. **Fallback:** alternate path after failure. **p95:** 95th-percentile latency. **Contract:** promised input/output behavior.
## References
- [Vertex AI model documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/models)
## Claim ledger
| Claim | Source | Fact or inference |
|---|---|---|
| Model catalogs expose different capabilities and constraints. | Google Cloud docs | Fact |
| Runtime routing should optimize multiple dimensions. | Systems inference | Inference |
## Detailed engineering walkthrough

A useful implementation starts by writing down the boundary between probabilistic work and deterministic work. The model may rank options, summarize evidence, or propose a next step, but a small service should own identity, authorization, persistence, and the definition of success. This boundary makes the system testable: a fixture can replace the model, a fake tool can return controlled failures, and an oracle can inspect the resulting state. It also makes incidents explainable because the trace can distinguish what was proposed from what was accepted.

For a local prototype, keep the state in a standard-library data structure or SQLite table. Give each task a stable identifier and record an event for every transition. Include the input hash, model and prompt version, selected route, tool name, sanitized arguments, policy decision, latency, and outcome. Never use a model-generated explanation as a permission check. Store only the minimum sensitive data needed to reproduce behavior, and make deletion and retention explicit from the start.

Design the happy path and at least four unhappy paths: malformed input, a transient dependency failure, a timeout after a possible side effect, and an adversarial or cross-tenant request. Each path should have a deterministic expected transition. Bound attempts, wall-clock time, output size, and money independently; one generous budget can hide an expensive failure. If uncertainty remains after a timeout, reconcile against the source of truth before retrying. If policy is unclear, pause for review rather than guessing.

Evaluate changes with a small matrix instead of one score. Compare task success, policy violations, p50 and p95 latency, tool calls, estimated cost, human edits, and escalation rate for simple, multi-step, stale-data, and tool-failure slices. Keep a holdout set and replay it after changing prompts, models, schemas, or routing. A capability improvement is not automatically a reliability or safety improvement. March’s primary discussions of AlphaGo and harmful-manipulation evaluation reinforce this separation: learned behavior can be useful while still requiring search, feedback, measurement, and human safeguards.

Operationally, expose dashboards for backlog, retries, denials, unknown errors, and terminal failures. Add alerts for sudden policy-denial changes, cross-tenant attempts, budget exhaustion, and p95 regressions. A kill switch should stop new side effects while allowing operators to inspect and reconcile in-flight tasks. Start with read-only or reversible actions, then expand authority only after the measured failure envelope is acceptable. These practices are engineering recommendations and inferences, not claims that a model or vendor guarantees safe autonomy.

## References and source use

Use the linked primary source to verify the release-specific claim before presenting it as fact. Use official protocol or platform documentation for implementation details, and label benchmark results with their task, population, and measurement method. When sources do not establish transfer to a production workload, say so explicitly. This keeps a March lesson useful to an SDE2 without turning an interesting demonstration into an unsupported deployment promise.
## Implementation design
This topic should be implemented as a small, inspectable system rather than a prompt-only demo. Begin with a contract that names inputs, outputs, authority, and success. Keep model suggestions separate from accepted actions. This allows deterministic test doubles to exercise policy and lets an operator answer what happened without reconstructing hidden conversation. A task identifier, correlation identifier, versioned configuration, and timestamp should travel through every event.

The minimum useful data model includes task status, owner or tenant, attempt count, deadline, budget remaining, and the last trusted observation. For any mutation, include an idempotency key and a before/after state check. For retrieved or human-provided content, include provenance and a trust classification. Filter scope before retrieval or ranking; semantic similarity is not authorization. Keep secrets out of prompts and redact them from logs. Define retention and deletion before collecting traces.

Build a deterministic local harness first. Use a fake world with a few records and tools that can return success, malformed output, a rate limit, a timeout, or a partial effect. Seed the scenario and record each event as JSONL. Assert both expected final state and forbidden events. A passing test can require a draft status and zero refund calls; a failure test can require a pause after two unknown errors. This is inexpensive and gives a stable baseline for model experiments.

When introducing a model, preserve the same harness and vary one factor at a time: model version, prompt template, retrieval policy, tool schema, or route. Report per-scenario and per-slice results, not just an average. Include success, unsafe-action rate, p50/p95 latency, tool-call count, estimated token cost, retry count, escalation rate, and human edits. A higher completion rate can coexist with worse safety or workload. Keep a hidden holdout and replay old incidents after every change.

Plan for operations. Set alerts on budget exhaustion, queue age, unknown errors, denied actions, cross-tenant attempts, and latency tails. Provide a kill switch that blocks new side effects, a drain mode for in-flight work, and reconciliation for ambiguous writes. Review sampled traces with access controls. Document who owns each terminal state and how correction is handled. Start with read-only, reversible, or draft-only actions; expand capability only when evidence supports it.

The March source context is deliberately narrow. DeepMind’s AlphaGo history supports claims about learned policy/value estimates working with search and environment feedback; it does not prove that a general business agent is reliable. DeepMind’s harmful-manipulation discussion supports studying human effects and safeguards; it does not establish a universal metric or safety guarantee. Treat official documentation as evidence for interfaces and published results as evidence for reported experiments. Mark deployment recommendations as engineering inference, and state where transfer remains uncertain.

A useful review asks five questions. What existed before this design, and what concrete capability changed? Which component owns authority and state? What happens on timeout, stale data, or adversarial input? Which metric would reveal harm even if task success rises? Can an operator pause, inspect, correct, and replay the task? If the lesson answers these with a runnable example and bounded test plan, it is ready for an SDE2 design review.
## Testing and operations
This topic should be implemented as a small, inspectable system rather than a prompt-only demo. Begin with a contract that names inputs, outputs, authority, and success. Keep model suggestions separate from accepted actions. This allows deterministic test doubles to exercise policy and lets an operator answer what happened without reconstructing hidden conversation. A task identifier, correlation identifier, versioned configuration, and timestamp should travel through every event.

The minimum useful data model includes task status, owner or tenant, attempt count, deadline, budget remaining, and the last trusted observation. For any mutation, include an idempotency key and a before/after state check. For retrieved or human-provided content, include provenance and a trust classification. Filter scope before retrieval or ranking; semantic similarity is not authorization. Keep secrets out of prompts and redact them from logs. Define retention and deletion before collecting traces.

Build a deterministic local harness first. Use a fake world with a few records and tools that can return success, malformed output, a rate limit, a timeout, or a partial effect. Seed the scenario and record each event as JSONL. Assert both expected final state and forbidden events. A passing test can require a draft status and zero refund calls; a failure test can require a pause after two unknown errors. This is inexpensive and gives a stable baseline for model experiments.

When introducing a model, preserve the same harness and vary one factor at a time: model version, prompt template, retrieval policy, tool schema, or route. Report per-scenario and per-slice results, not just an average. Include success, unsafe-action rate, p50/p95 latency, tool-call count, estimated token cost, retry count, escalation rate, and human edits. A higher completion rate can coexist with worse safety or workload. Keep a hidden holdout and replay old incidents after every change.

Plan for operations. Set alerts on budget exhaustion, queue age, unknown errors, denied actions, cross-tenant attempts, and latency tails. Provide a kill switch that blocks new side effects, a drain mode for in-flight work, and reconciliation for ambiguous writes. Review sampled traces with access controls. Document who owns each terminal state and how correction is handled. Start with read-only, reversible, or draft-only actions; expand capability only when evidence supports it.

The March source context is deliberately narrow. DeepMind’s AlphaGo history supports claims about learned policy/value estimates working with search and environment feedback; it does not prove that a general business agent is reliable. DeepMind’s harmful-manipulation discussion supports studying human effects and safeguards; it does not establish a universal metric or safety guarantee. Treat official documentation as evidence for interfaces and published results as evidence for reported experiments. Mark deployment recommendations as engineering inference, and state where transfer remains uncertain.

A useful review asks five questions. What existed before this design, and what concrete capability changed? Which component owns authority and state? What happens on timeout, stale data, or adversarial input? Which metric would reveal harm even if task success rises? Can an operator pause, inspect, correct, and replay the task? If the lesson answers these with a runnable example and bounded test plan, it is ready for an SDE2 design review.
## Review checklist
This topic should be implemented as a small, inspectable system rather than a prompt-only demo. Begin with a contract that names inputs, outputs, authority, and success. Keep model suggestions separate from accepted actions. This allows deterministic test doubles to exercise policy and lets an operator answer what happened without reconstructing hidden conversation. A task identifier, correlation identifier, versioned configuration, and timestamp should travel through every event.

The minimum useful data model includes task status, owner or tenant, attempt count, deadline, budget remaining, and the last trusted observation. For any mutation, include an idempotency key and a before/after state check. For retrieved or human-provided content, include provenance and a trust classification. Filter scope before retrieval or ranking; semantic similarity is not authorization. Keep secrets out of prompts and redact them from logs. Define retention and deletion before collecting traces.

Build a deterministic local harness first. Use a fake world with a few records and tools that can return success, malformed output, a rate limit, a timeout, or a partial effect. Seed the scenario and record each event as JSONL. Assert both expected final state and forbidden events. A passing test can require a draft status and zero refund calls; a failure test can require a pause after two unknown errors. This is inexpensive and gives a stable baseline for model experiments.

When introducing a model, preserve the same harness and vary one factor at a time: model version, prompt template, retrieval policy, tool schema, or route. Report per-scenario and per-slice results, not just an average. Include success, unsafe-action rate, p50/p95 latency, tool-call count, estimated token cost, retry count, escalation rate, and human edits. A higher completion rate can coexist with worse safety or workload. Keep a hidden holdout and replay old incidents after every change.

Plan for operations. Set alerts on budget exhaustion, queue age, unknown errors, denied actions, cross-tenant attempts, and latency tails. Provide a kill switch that blocks new side effects, a drain mode for in-flight work, and reconciliation for ambiguous writes. Review sampled traces with access controls. Document who owns each terminal state and how correction is handled. Start with read-only, reversible, or draft-only actions; expand capability only when evidence supports it.

The March source context is deliberately narrow. DeepMind’s AlphaGo history supports claims about learned policy/value estimates working with search and environment feedback; it does not prove that a general business agent is reliable. DeepMind’s harmful-manipulation discussion supports studying human effects and safeguards; it does not establish a universal metric or safety guarantee. Treat official documentation as evidence for interfaces and published results as evidence for reported experiments. Mark deployment recommendations as engineering inference, and state where transfer remains uncertain.

A useful review asks five questions. What existed before this design, and what concrete capability changed? Which component owns authority and state? What happens on timeout, stale data, or adversarial input? Which metric would reveal harm even if task success rises? Can an operator pause, inspect, correct, and replay the task? If the lesson answers these with a runnable example and bounded test plan, it is ready for an SDE2 design review.
## Extended local plan
This topic should be implemented as a small, inspectable system rather than a prompt-only demo. Begin with a contract that names inputs, outputs, authority, and success. Keep model suggestions separate from accepted actions. This allows deterministic test doubles to exercise policy and lets an operator answer what happened without reconstructing hidden conversation. A task identifier, correlation identifier, versioned configuration, and timestamp should travel through every event.

The minimum useful data model includes task status, owner or tenant, attempt count, deadline, budget remaining, and the last trusted observation. For any mutation, include an idempotency key and a before/after state check. For retrieved or human-provided content, include provenance and a trust classification. Filter scope before retrieval or ranking; semantic similarity is not authorization. Keep secrets out of prompts and redact them from logs. Define retention and deletion before collecting traces.

Build a deterministic local harness first. Use a fake world with a few records and tools that can return success, malformed output, a rate limit, a timeout, or a partial effect. Seed the scenario and record each event as JSONL. Assert both expected final state and forbidden events. A passing test can require a draft status and zero refund calls; a failure test can require a pause after two unknown errors. This is inexpensive and gives a stable baseline for model experiments.

When introducing a model, preserve the same harness and vary one factor at a time: model version, prompt template, retrieval policy, tool schema, or route. Report per-scenario and per-slice results, not just an average. Include success, unsafe-action rate, p50/p95 latency, tool-call count, estimated token cost, retry count, escalation rate, and human edits. A higher completion rate can coexist with worse safety or workload. Keep a hidden holdout and replay old incidents after every change.

Plan for operations. Set alerts on budget exhaustion, queue age, unknown errors, denied actions, cross-tenant attempts, and latency tails. Provide a kill switch that blocks new side effects, a drain mode for in-flight work, and reconciliation for ambiguous writes. Review sampled traces with access controls. Document who owns each terminal state and how correction is handled. Start with read-only, reversible, or draft-only actions; expand capability only when evidence supports it.

The March source context is deliberately narrow. DeepMind’s AlphaGo history supports claims about learned policy/value estimates working with search and environment feedback; it does not prove that a general business agent is reliable. DeepMind’s harmful-manipulation discussion supports studying human effects and safeguards; it does not establish a universal metric or safety guarantee. Treat official documentation as evidence for interfaces and published results as evidence for reported experiments. Mark deployment recommendations as engineering inference, and state where transfer remains uncertain.

A useful review asks five questions. What existed before this design, and what concrete capability changed? Which component owns authority and state? What happens on timeout, stale data, or adversarial input? Which metric would reveal harm even if task success rises? Can an operator pause, inspect, correct, and replay the task? If the lesson answers these with a runnable example and bounded test plan, it is ready for an SDE2 design review.
