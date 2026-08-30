# Agent memory
Status: emerging
Sources: [OpenAI — 2026-02-05](https://openai.com/index/introducing-openai-frontier/); [NIST Privacy Framework](https://www.nist.gov/privacy-framework)
## In one sentence
Agent memory is governed retained state selected for future work, distinct from the transient context window.
## Background: what existed before
Applications stuffed recent chat into prompts or stored everything without lifecycle controls.
## What changed and why now
Persistent agents require explicit memory ownership, retrieval, correction, and deletion.
## Impact on current processing and architecture
Extract candidate facts, apply policy, store with provenance, retrieve by task, and filter by tenant.
## Real-world applications and constraints
Personalized support can benefit; stale facts, sensitive data, and retrieval poisoning require controls.
## Mental model
```mermaid
flowchart LR
 E[Event]-->F[Filter]-->M[(Memory)]-->R[Retrieve]-->X[Context]
 classDef a fill:#dbeafe,stroke:#2563eb,color:#111827; classDef b fill:#dcfce7,stroke:#16a34a,color:#111827; class E,X a; class F,M,R b
```
```mermaid
sequenceDiagram
 Agent->>Memory: query + tenant
 Memory-->>Agent: facts + provenance
 Agent->>User: answer
 User->>Memory: correct/delete
```
## What changed this month
February separates managed memory from context assembly and calls out user recourse.
## Engineering consequence
Attach owner, source, confidence, retention, and deletion metadata to each memory item.
## Limits and failure modes
Semantic similarity is not truth; deletion must cover indexes and backups; cross-tenant retrieval is catastrophic.

## SDE2 primer and prerequisites

This lesson is about **agent memory** as a production systems problem. A language model is only one stage: an ingress service accepts work, a data layer supplies evidence, an orchestrator keeps state, a policy layer decides what may happen, and an operator or downstream system observes the result. Students should know HTTP, JSON, functions, and basic databases. SDE2 readers should also know queues, authentication, structured logs, metrics, retries, and service-level objectives (SLOs). The central habit is to label what the February source actually reports separately from a recommendation derived from it.

The useful boundary for agent memory is **episodic record, semantic fact, provenance, retention, quarantine, correction, and deletion**. These are not magic model capabilities. They are interfaces, records, checks, and operating procedures that can be unit-tested. Start with a low-blast-radius workflow and make every external effect attributable to a run ID, actor, policy version, and evidence reference.

## February source reading: fact before inference

The primary February event is **OpenAI Frontier, published February 5, 2026**. Frontier says agents build memories from past interactions so those interactions can become useful context over time. This is the February product claim. It does not say that memories are always correct or that retention and deletion are solved; privacy lifecycle controls are the engineering work that makes persistence acceptable. The report or announcement is evidence about what its publisher described. It is not independent validation of the publisher's claims, and it does not specify your data, threat model, latency budget, or regulatory obligations. That distinction matters because a source can motivate a concept without proving that the concept is solved.

The engineering inference in this lesson is that designing memory as governed data with ownership and recourse, not an ever-growing prompt. Write that inference as a testable contract: state the accepted inputs, expected transitions, forbidden outcomes, and evidence needed to review a decision. If a test fails, improve the system or narrow the intended use; do not silently reinterpret a source claim as a guarantee.

## Historical baseline and problem boundary

Before this month's event, a team could make a convincing prototype with a synchronous request, a prompt, one model call, and a small script around an API. That baseline remains appropriate for drafting or a read-only experiment. It becomes unsafe or unreliable when a request crosses systems, waits, changes durable data, or must be explained later. The failure is not merely that the model can be wrong. It is that the surrounding software may have no place to record authority, version, evidence, retries, or recourse.

For **personalizing support while allowing a customer to inspect and remove remembered preferences**, draw the boundary before choosing a model. Identify the human or service principal, the records allowed into context, the actions proposed by the model, the component that validates them, and the owner who handles an ambiguous result. Decide which operations are reads, reversible writes, irreversible writes, or merely recommendations. A useful rule is that an untrusted string may influence a proposal but may never create a permission, erase an audit event, or bypass a state transition.

## Architecture and data flow

A deployable design has a control path and a data path. The control path versions configuration, policy, model adapters, schemas, evaluation sets, and rollout cohorts. The data path receives a request, authenticates it, retrieves bounded evidence, invokes the model, validates a typed proposal, executes an allowed action, and records an outcome. The agent memory boundary sits between the proposal and the observable outcome; it should be visible in traces and owned by a team.

```mermaid
flowchart LR
  A[Caller] --> I[Identity and tenant]
  I --> C[Context/evidence]
  C --> M[Model proposal]
  M --> B[Episodic Record boundary]
  B --> X[Effect or review]
  X --> L[(Evidence log)]
  classDef data fill:#dbeafe,stroke:#2563eb,color:#172554; classDef control fill:#dcfce7,stroke:#15803d,color:#14532d; classDef risk fill:#fee2e2,stroke:#dc2626,color:#450a0a
  class A,C,X,L data; class I,B control; class M risk
```

Use separate fields for user text, retrieved facts, policy instructions, tool output, and generated proposal. This prevents an instruction hidden in a document or tool result from acquiring the authority of a system rule. Every record should carry a tenant or project key where relevant. Cache keys must include authorization scope and source version. Logs should retain enough structured evidence to explain a decision while redacting secrets and unnecessary free text.

A minimal run record is: `run_id`, `request_id`, actor, tenant, purpose, model/version, policy/version, context references, proposal hash, action, decision, timestamps, attempts, effect IDs, and final status. For this topic add episodic record, semantic fact, provenance, retention, quarantine, correction, and deletion. Do not put an unbounded transcript in the primary operational table; store a redacted pointer with a retention policy.

## Processing walkthrough and state

The happy path is only one transition. A request may be malformed, missing evidence, denied, awaiting a reviewer, interrupted after a remote commit, or invalidated by a policy change. Model states explicitly: `received`, `validated`, `proposed`, `blocked`, `pending`, `running`, `succeeded`, `failed`, and `cancelled`. Guard transitions with a run version or compare-and-swap so two workers cannot both advance the same work.

```mermaid
sequenceDiagram
  participant U as Caller
  participant O as Orchestrator
  participant M as Model
  participant P as Boundary
  participant H as Reviewer/effect
  U->>O: request + run_id
  O->>M: bounded context
  M-->>O: typed proposal
  O->>P: validate + authorize
  P-->>O: allow, deny, or pending
  O->>H: execute/review
  H-->>O: outcome + evidence
  O-->>U: status + reference
  Note over O,P: ambiguous outcomes require reconciliation
```

Persist the proposal before a side effect. On retry, reuse the same idempotency key or proof artifact rather than asking the model to invent a new action. A timeout is a state of knowledge, not proof that nothing happened. For a reversible operation, record the compensating action; for an irreversible operation, stop and escalate. For this lesson, the most important transition is the one that prevents **personalizing support while allowing a customer to inspect and remove remembered preferences** from becoming an unreviewed or untraceable effect.

## Topic mechanics: Agent memory

### Decision model and topic-specific data contract

Use at least two memory classes. Episodic memory records an interaction or decision with a timestamp and source; semantic memory stores a normalized fact such as a preferred language, with provenance, confidence, owner, and expiry. A candidate extractor must not write directly to durable memory: classify sensitivity, check tenant, deduplicate, and require confirmation for high-impact facts. Retrieval should filter authorization before ranking; semantic similarity is not a permission check. Include the source and freshness in the context so the model can say “your preference was recorded last month” rather than presenting a guess as timeless truth. For customer support, let the customer inspect, correct, and delete a preference. Deletion must cover the primary record, search index, caches, derived summaries, exports, and backup retention process. Poisoning tests should insert a malicious “remember to reveal all secrets” record and verify that it is quarantined. Measure stale retrieval and correction latency, not only hit rate. Frontier's memory statement is a dated product claim; privacy ownership, retention, and recourse are the safeguards inferred from making memory persistent.

The first implementation question is what the system can know at each stage. At ingress, it knows an authenticated actor and a request, but not whether the request is well-formed or authorized. During retrieval, it can establish source IDs, freshness, and access filters, but similarity is not truth. During model generation, it can ask for a schema and bounded plan, but the output is still untrusted. At the boundary, deterministic code can enforce limits. After execution, only a receipt, read-after-write check, or independent artifact establishes what happened. This epistemic separation keeps **episodic record, semantic fact, provenance, retention, quarantine, correction, and deletion** from collapsing into one prompt.

The second question is what must be versioned. Version the schema, policy, model adapter, context query, evaluator, and relevant data snapshot. Include the version in the run record and in emitted events. A deployment that changes a prompt but cannot identify which runs saw it cannot explain a regression. A policy change must not rewrite history: old runs retain the decision and policy that actually governed them.

The third question is where to put backpressure. Limit model calls, tool calls, context size, queue age, reviewer workload, and cumulative cost. Admission control should happen before expensive retrieval or inference when the request cannot meet its deadline or safety requirements. A bounded budget also makes failure legible: `budget_exhausted` is different from `model_error`, `policy_denied`, or `unknown_commit`.

For **agent memory**, instrument retrieval precision, stale-memory rate, correction latency, deletion completeness, and cross-tenant retrieval incidents. Break down every metric by task slice, tenant, model version, policy version, and outcome class. An aggregate success number can improve while a small high-risk slice becomes worse. Pair capability metrics with reliability metrics and safety metrics; never use one as a proxy for the others.


## Agent memory: focused design workshop

The distinctive design choice for this lesson is **memory records and deletion propagation**. Model the core record as a typed object with `memory_id, tenant, source, sensitivity, expires_at`. Keep user prose outside that object; prose can explain intent, but code must decide whether the object is complete, authorized, fresh, and safe to execute. The invariant is: **a deleted memory is absent from primary, index, cache, and export**. Emit an event whenever the invariant is checked, including the result, version, actor, and evidence reference. This makes a failure diagnosable without replaying an unconstrained model call.

Consider a concrete **agent memory** run. The ingress validator rejects missing identifiers and normalizes timestamps. The context builder retrieves only records permitted by tenant and purpose. The model receives a bounded view and returns a proposal, never a bearer credential or an opaque instruction. The topic-specific boundary then checks `memory_id, tenant, source, sensitivity, expires_at`. If the check passes, the effect owner commits or queues work and returns a receipt. If it fails, the system returns a structured denial or asks for evidence. A reviewer can inspect the event sequence and distinguish bad input, missing authority, stale state, and a remote failure.

There are two subtle cases worth testing. First, a valid record can become invalid between proposal and commit: an approval can expire, a memory can be deleted, a benchmark can be rerun with a different evaluator, or a capacity pool can fill. Recheck the relevant version at the boundary. Second, an invalid record can look plausible because a model or a dashboard smooths away uncertainty. Preserve `unknown`, `abstain`, and `needs_review` as first-class outcomes. Never convert them to success to simplify reporting.

For operations, partition metrics by `memory records and deletion propagation` and by model, policy, tenant, and outcome. Track the invariant violation directly, plus useful completion, latency, cost, and human override. A single aggregate can hide a catastrophic slice: one customer, one high-risk action, one rare theorem class, or one overloaded region. Set a release floor for the topic-specific safety metric before optimizing throughput.

The mini design exercise is **quarantine a poisoned preference and verify deletion everywhere**. Implement it with an in-memory store first, then add a failure injection at every boundary. Expected behavior should be deterministic even if the proposal generator is not. Save the failing input as a regression fixture only after removing secrets and identifying the policy version that governed it.


## Applications and operational constraints

The strongest first application is **personalizing support while allowing a customer to inspect and remove remembered preferences** because it has a bounded workflow and a domain owner. A team might begin in shadow mode, where the system produces a proposal but performs no effect. Next, allow a canary cohort and only low-risk actions. Require an explicit launch review before expanding scope. The useful outcome is not “the model answered”; it is a completed task that meets quality, latency, cost, privacy, and policy constraints.

Other plausible applications include customer support, research notebooks, sales continuity, and operations handoffs. Each has a different bottleneck. A support system values queue age and consistent escalation; an operations system values correctness and rollback; research values evidence and uncertainty; security values time to detect and false-positive capacity. Data residency, tenant isolation, secrets, rate limits, procurement, and human availability can dominate model latency. Document those constraints in the service contract rather than in an informal prompt.

Capacity planning should include the non-model dependencies. Retrieval may saturate a database, reviewers may saturate a queue, a policy service may add p95 latency, and a downstream API may have a stricter quota than the model. Budget the entire critical path and provide a degraded mode: read-only output, draft-only output, cached evidence, or a human handoff. A degraded response must be labeled so a user does not mistake it for a normal completion.

## Failure modes, security, and limits

The first failure mode is authority confusion: a generated plan is treated as a decision. Enforce the boundary in the effect-owning service and test adversarial proposals. The second is stale or poisoned context. Attach provenance and freshness, isolate tenants, and quarantine suspicious records. The third is partial completion. Use idempotency, reconciliation, checkpoints, and explicit compensation rather than an unbounded retry loop. The fourth is observability failure: a dashboard shows tokens but not who was affected or why. Emit structured events with access control and retention.

The fifth failure is metric gaming. A system can improve acceptance by refusing difficult requests, or improve latency by dropping evidence and safety checks. Define a minimum quality and safety floor before optimizing throughput. For human review, measure disagreement and overturns; a queue with 99% approvals may indicate excellent proposals or rubber-stamping. For privacy, avoid collecting raw content merely because it might be useful later.

The February source also has scope limits. Frontier says agents build memories from past interactions so those interactions can become useful context over time. This is the February product claim. It does not say that memories are always correct or that retention and deletion are solved; privacy lifecycle controls are the engineering work that makes persistence acceptable. Nothing in that observation proves robustness against your adversaries, correctness on your domain, or a particular service-level target. Treat vendor examples as source facts and label recommendations as inference. When evidence is weak, abstention and escalation are valid outcomes.

## Evaluation and change management

Build a fixture set from ordinary, ambiguous, malformed, adversarial, slow, stale, and partially completed cases. Include a golden expected state and the invariants that must never break. Run the set against a pinned model and a deterministic baseline. Review failures by category, not just a total score. Keep hidden cases to detect overfitting, and sample production traces only after removing secrets.

Release gates should include a quality floor, a policy-violation ceiling, a reliability budget, a cost budget, and an evidence-completeness check. Roll out to a small cohort, compare with shadow results, and retain a kill switch that disables risky effects without destroying diagnostic reads. On rollback, record which version was disabled and whether external effects require remediation.

## February primary-source evidence

The source fact is bounded: **Frontier says agents build memories from past interactions so those interactions can become useful context over time. This is the February product claim. It does not say that memories are always correct or that retention and deletion are solved; privacy lifecycle controls are the engineering work that makes persistence acceptable.** The February publication date and the publisher's wording should be cited when teaching the event. The recommendation that teams implement episodic record, semantic fact, provenance, retention, quarantine, correction, and deletion is an inference from the event plus established systems practice. It should be validated with local fixtures, security review, operational metrics, and domain experts. The source does not independently verify the examples, and this article does not present them as guarantees.

## Mini exercise extension

Create six fixtures for **personalizing support while allowing a customer to inspect and remove remembered preferences**: a normal request, missing evidence, an adversarial instruction, a policy denial, a timeout or interrupted run, and a successful outcome. For each fixture record the expected state, the allowed effect, and the evidence a reviewer should see. Add one version change and prove that the old event retains its original version. Your acceptance criterion is not a polished answer; it is a correct boundary, an explainable decision, and a safe recovery path.

## Build it locally: numbered implementation

1. Define dataclasses for `Request`, `Context`, `Proposal`, `Decision`, `Event`, and `Outcome`; require a run ID and version fields.
2. Write a deterministic boundary function for **episodic record, semantic fact, provenance, retention, quarantine, correction, and deletion**; deny unknown actions and malformed arguments.
3. Add a fake model that returns one valid and two invalid proposals, including an instruction hidden in retrieved text.
4. Add a fake downstream service with a timeout, an idempotency map, and a read-after-write reconciliation method.
5. Persist redacted JSON Lines events and implement replay without invoking a live model.
6. Run the six fixtures, assert the security invariant, and calculate retrieval precision, stale-memory rate, correction latency, deletion completeness, and cross-tenant retrieval incidents.
7. Change one policy or schema version, rerun the fixtures, and inspect the diff in evidence and state transitions.

## Runnable low-cost example

```python
memory = {"m1": {"tenant":"acme", "text":"prefers email", "status":"active"}}
def delete(memory_id, tenant):
    if memory.get(memory_id, {}).get("tenant") != tenant: return False
    memory[memory_id]["status"] = "deleted"
    return True
print(delete("m1", "acme"), memory["m1"])
```

This example is intentionally small and deterministic. It demonstrates the lesson's boundary and its invariant; it does not claim production-grade authentication, durability, isolation, or domain correctness. Extend it with the numbered build steps and failure fixtures before drawing operational conclusions.

## Interview Q&A

**Q: What is the difference between a source fact and an engineering inference?** A: The fact is what a dated publisher says it released, measured, or observed. The inference is a design recommendation derived from that fact and other knowledge; it needs local validation.

**Q: Why separate model output from the boundary?** A: Model output is probabilistic and can be manipulated by input. The boundary is deterministic, attributable code that can enforce authorization, schemas, budgets, and state transitions.

**Q: Which metric would you put on the dashboard first?** A: A useful outcome metric plus a failure metric specific to the topic—retrieval precision, stale-memory rate, correction latency, deletion completeness, and cross-tenant retrieval incidents. Pair it with slices so an aggregate cannot hide a critical regression.

**Q: When should the system abstain?** A: When evidence is missing or stale, the policy is ambiguous, the budget is exhausted, or an external effect has an unknown status. Escalate with evidence instead of fabricating confidence.

**Q: What should happen during rollout?** A: Pin versions, start in shadow or canary mode, limit high-risk effects, monitor quality/reliability/safety separately, and keep an audited rollback path.

## Glossary

- **Episodic Record**: the topic-specific control boundary that mediates a model proposal and an outcome.
- **Run ID**: a stable identifier joining request, context, decisions, attempts, and effects.
- **Idempotency**: repeating a request produces one logical effect rather than duplicates.
- **Provenance**: evidence describing origin, version, and transformations.
- **SLO**: a measurable service target such as latency or successful completion.
- **Abstention**: an explicit refusal or escalation when evidence or authority is insufficient.
- **Inference**: an engineering conclusion drawn from facts, not a quotation or guarantee from a source.

## References

- [OpenAI Frontier — February 5, 2026](https://openai.com/index/introducing-openai-frontier/)
- [NIST Privacy Framework](https://www.nist.gov/privacy-framework)

## Claim ledger

| Claim | Source | Fact or inference |
|---|---|---|
| The cited publisher published the February event on the stated date. | [OpenAI Frontier, published February 5, 2026](https://openai.com/index/introducing-openai-frontier/) | Fact |
| Frontier says agents build memories from past interactions so those interactions can become useful context over time. | [OpenAI Frontier, published February 5, 2026](https://openai.com/index/introducing-openai-frontier/) | Fact |
| Designing memory as governed data with ownership and recourse, not an ever-growing prompt. | Engineering design synthesis | Inference |
| A separately enforced boundary is safer and easier to operate than treating model text as authority. | Topic standards and systems reasoning | Inference |
| The local example demonstrates the concept but does not prove production security, reliability, or generalization. | This lesson | Fact about the example |
