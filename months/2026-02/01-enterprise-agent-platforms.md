# Enterprise agent platforms
Status: emerging
Sources: [OpenAI — 2026-02-05](https://openai.com/index/introducing-openai-frontier/); [NIST AI RMF — 2023-01-26](https://www.nist.gov/itl/ai-risk-management-framework)

## In one sentence
An enterprise agent platform supplies shared context, tools, permissions, feedback, and management around otherwise stateless model calls.
## Background: what existed before
Teams hand-wired chat prompts, API keys, queues, and audit logs; each agent had a different control plane.
## What changed and why now
Frontier describes a shared system for deploying and governing agents; the change is operational integration, not a claim that models became autonomous.
## Impact on current processing and architecture
Requests now pass through identity, policy, context retrieval, model, tool gateway, and telemetry layers.
## Real-world applications and constraints
Useful for support triage and finance research. Tenant isolation, latency budgets, data residency, and per-tool cost remain constraints.
## Mental model
```mermaid
flowchart LR
 U[User]-->P[Policy]-->C[Context]-->M[Model]-->G[Tool gateway]-->S[Systems]
 classDef io fill:#dbeafe,stroke:#2563eb,color:#111827; classDef ctl fill:#dcfce7,stroke:#16a34a,color:#111827; class U,S io; class P,C,M,G ctl
```
```mermaid
sequenceDiagram
 participant A as Agent
 participant X as Control plane
 participant T as Tool
 A->>X: plan + identity
 X-->>A: allowed context
 A->>T: typed request
 T-->>X: result + audit event
 classDef note fill:#fef3c7,stroke:#d97706,color:#111827
```
## What changed this month
The February map treats agent platforms as a first-class architectural boundary, prompted by Frontier's enterprise-agent framing.
## Engineering consequence
Design one policy and observability plane; keep model adapters replaceable.
## Limits and failure modes
Centralization can create an outage or privilege concentration; shared context can leak tenants; model output is not authorization.

## SDE2 primer and prerequisites

This lesson is about **enterprise agent platforms** as a production systems problem. A language model is only one stage: an ingress service accepts work, a data layer supplies evidence, an orchestrator keeps state, a policy layer decides what may happen, and an operator or downstream system observes the result. Students should know HTTP, JSON, functions, and basic databases. SDE2 readers should also know queues, authentication, structured logs, metrics, retries, and service-level objectives (SLOs). The central habit is to label what the February source actually reports separately from a recommendation derived from it.

The useful boundary for enterprise agent platforms is **agent registry, semantic context layer, adapter, tenant control plane, and audit stream**. These are not magic model capabilities. They are interfaces, records, checks, and operating procedures that can be unit-tested. Start with a low-blast-radius workflow and make every external effect attributable to a run ID, actor, policy version, and evidence reference.

## February source reading: fact before inference

The primary February event is **OpenAI Frontier, published February 5, 2026**. OpenAI says Frontier is a platform to build, deploy, and manage agents; it describes shared context, onboarding, feedback, and explicit identity and permissions. The post reports, as customer examples, production optimization falling from six weeks to one day, more than 90% additional salesperson time, and output increasing by up to 5% at an energy producer. These are reported examples, not independently audited benchmarks. The report or announcement is evidence about what its publisher described. It is not independent validation of the publisher's claims, and it does not specify your data, threat model, latency budget, or regulatory obligations. That distinction matters because a source can motivate a concept without proving that the concept is solved.

The engineering inference in this lesson is that turning a collection of clever pilots into a governed internal platform. Write that inference as a testable contract: state the accepted inputs, expected transitions, forbidden outcomes, and evidence needed to review a decision. If a test fails, improve the system or narrow the intended use; do not silently reinterpret a source claim as a guarantee.

## Historical baseline and problem boundary

Before this month's event, a team could make a convincing prototype with a synchronous request, a prompt, one model call, and a small script around an API. That baseline remains appropriate for drafting or a read-only experiment. It becomes unsafe or unreliable when a request crosses systems, waits, changes durable data, or must be explained later. The failure is not merely that the model can be wrong. It is that the surrounding software may have no place to record authority, version, evidence, retries, or recourse.

For **root-cause investigation for a hardware manufacturer**, draw the boundary before choosing a model. Identify the human or service principal, the records allowed into context, the actions proposed by the model, the component that validates them, and the owner who handles an ambiguous result. Decide which operations are reads, reversible writes, irreversible writes, or merely recommendations. A useful rule is that an untrusted string may influence a proposal but may never create a permission, erase an audit event, or bypass a state transition.

## Architecture and data flow

A deployable design has a control path and a data path. The control path versions configuration, policy, model adapters, schemas, evaluation sets, and rollout cohorts. The data path receives a request, authenticates it, retrieves bounded evidence, invokes the model, validates a typed proposal, executes an allowed action, and records an outcome. The enterprise agent platforms boundary sits between the proposal and the observable outcome; it should be visible in traces and owned by a team.

```mermaid
flowchart LR
  A[Caller] --> I[Identity and tenant]
  I --> C[Context/evidence]
  C --> M[Model proposal]
  M --> B[Agent Registry boundary]
  B --> X[Effect or review]
  X --> L[(Evidence log)]
  classDef data fill:#dbeafe,stroke:#2563eb,color:#172554; classDef control fill:#dcfce7,stroke:#15803d,color:#14532d; classDef risk fill:#fee2e2,stroke:#dc2626,color:#450a0a
  class A,C,X,L data; class I,B control; class M risk
```

Use separate fields for user text, retrieved facts, policy instructions, tool output, and generated proposal. This prevents an instruction hidden in a document or tool result from acquiring the authority of a system rule. Every record should carry a tenant or project key where relevant. Cache keys must include authorization scope and source version. Logs should retain enough structured evidence to explain a decision while redacting secrets and unnecessary free text.

A minimal run record is: `run_id`, `request_id`, actor, tenant, purpose, model/version, policy/version, context references, proposal hash, action, decision, timestamps, attempts, effect IDs, and final status. For this topic add agent registry, semantic context layer, adapter, tenant control plane, and audit stream. Do not put an unbounded transcript in the primary operational table; store a redacted pointer with a retention policy.

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

Persist the proposal before a side effect. On retry, reuse the same idempotency key or proof artifact rather than asking the model to invent a new action. A timeout is a state of knowledge, not proof that nothing happened. For a reversible operation, record the compensating action; for an irreversible operation, stop and escalate. For this lesson, the most important transition is the one that prevents **root-cause investigation for a hardware manufacturer** from becoming an unreviewed or untraceable effect.

## Topic mechanics: Enterprise agent platforms

### Decision model and topic-specific data contract

A platform team should publish an agent registry, not merely a prompt catalog. A registry entry names the owner, tenant scope, data classes, model adapter, tool set, escalation policy, SLO, cost center, evaluation set, and kill switch. The semantic context layer should expose business entities and relationships through a stable contract while preserving the source system's authorization. A context answer therefore includes source IDs and freshness, not just embedded text. The adapter turns that context into a model-specific request and returns a platform-neutral proposal. This lets a team replace a model without granting a new tool or changing the audit schema. The tool gateway is where schemas, policy, rate limits, and idempotency meet. Its events should be consumable by security, finance, and service owners without exposing every prompt. The trade-off is centralization: common controls reduce drift, but a broken control plane can block every tenant. Use regional replicas, cached read-only metadata, and a break-glass path with a short expiry. For the manufacturer example reported by OpenAI, measure investigation time and accepted root-cause actions, not simply how many agents were registered.

The first implementation question is what the system can know at each stage. At ingress, it knows an authenticated actor and a request, but not whether the request is well-formed or authorized. During retrieval, it can establish source IDs, freshness, and access filters, but similarity is not truth. During model generation, it can ask for a schema and bounded plan, but the output is still untrusted. At the boundary, deterministic code can enforce limits. After execution, only a receipt, read-after-write check, or independent artifact establishes what happened. This epistemic separation keeps **agent registry, semantic context layer, adapter, tenant control plane, and audit stream** from collapsing into one prompt.

The second question is what must be versioned. Version the schema, policy, model adapter, context query, evaluator, and relevant data snapshot. Include the version in the run record and in emitted events. A deployment that changes a prompt but cannot identify which runs saw it cannot explain a regression. A policy change must not rewrite history: old runs retain the decision and policy that actually governed them.

The third question is where to put backpressure. Limit model calls, tool calls, context size, queue age, reviewer workload, and cumulative cost. Admission control should happen before expensive retrieval or inference when the request cannot meet its deadline or safety requirements. A bounded budget also makes failure legible: `budget_exhausted` is different from `model_error`, `policy_denied`, or `unknown_commit`.

For **enterprise agent platforms**, instrument tenant isolation errors, time to onboard a tool, useful completion rate, policy-denial rate, and cost per completed business outcome. Break down every metric by task slice, tenant, model version, policy version, and outcome class. An aggregate success number can improve while a small high-risk slice becomes worse. Pair capability metrics with reliability metrics and safety metrics; never use one as a proxy for the others.


## Enterprise agent platforms: focused design workshop

The distinctive design choice for this lesson is **registry and tenant routing**. Model the core record as a typed object with `agent_id, tenant, owner, tools, model_version`. Keep user prose outside that object; prose can explain intent, but code must decide whether the object is complete, authorized, fresh, and safe to execute. The invariant is: **registry entries must name owner, tools, data classes, and policy version**. Emit an event whenever the invariant is checked, including the result, version, actor, and evidence reference. This makes a failure diagnosable without replaying an unconstrained model call.

Consider a concrete **enterprise agent platforms** run. The ingress validator rejects missing identifiers and normalizes timestamps. The context builder retrieves only records permitted by tenant and purpose. The model receives a bounded view and returns a proposal, never a bearer credential or an opaque instruction. The topic-specific boundary then checks `agent_id, tenant, owner, tools, model_version`. If the check passes, the effect owner commits or queues work and returns a receipt. If it fails, the system returns a structured denial or asks for evidence. A reviewer can inspect the event sequence and distinguish bad input, missing authority, stale state, and a remote failure.

There are two subtle cases worth testing. First, a valid record can become invalid between proposal and commit: an approval can expire, a memory can be deleted, a benchmark can be rerun with a different evaluator, or a capacity pool can fill. Recheck the relevant version at the boundary. Second, an invalid record can look plausible because a model or a dashboard smooths away uncertainty. Preserve `unknown`, `abstain`, and `needs_review` as first-class outcomes. Never convert them to success to simplify reporting.

For operations, partition metrics by `registry and tenant routing` and by model, policy, tenant, and outcome. Track the invariant violation directly, plus useful completion, latency, cost, and human override. A single aggregate can hide a catastrophic slice: one customer, one high-risk action, one rare theorem class, or one overloaded region. Set a release floor for the topic-specific safety metric before optimizing throughput.

The mini design exercise is **reject an unregistered agent before it can retrieve data**. Implement it with an in-memory store first, then add a failure injection at every boundary. Expected behavior should be deterministic even if the proposal generator is not. Save the failing input as a regression fixture only after removing secrets and identifying the policy version that governed it.


## Applications and operational constraints

The strongest first application is **root-cause investigation for a hardware manufacturer** because it has a bounded workflow and a domain owner. A team might begin in shadow mode, where the system produces a proposal but performs no effect. Next, allow a canary cohort and only low-risk actions. Require an explicit launch review before expanding scope. The useful outcome is not “the model answered”; it is a completed task that meets quality, latency, cost, privacy, and policy constraints.

Other plausible applications include support triage, finance research, manufacturing diagnostics, and internal operations. Each has a different bottleneck. A support system values queue age and consistent escalation; an operations system values correctness and rollback; research values evidence and uncertainty; security values time to detect and false-positive capacity. Data residency, tenant isolation, secrets, rate limits, procurement, and human availability can dominate model latency. Document those constraints in the service contract rather than in an informal prompt.

Capacity planning should include the non-model dependencies. Retrieval may saturate a database, reviewers may saturate a queue, a policy service may add p95 latency, and a downstream API may have a stricter quota than the model. Budget the entire critical path and provide a degraded mode: read-only output, draft-only output, cached evidence, or a human handoff. A degraded response must be labeled so a user does not mistake it for a normal completion.

## Failure modes, security, and limits

The first failure mode is authority confusion: a generated plan is treated as a decision. Enforce the boundary in the effect-owning service and test adversarial proposals. The second is stale or poisoned context. Attach provenance and freshness, isolate tenants, and quarantine suspicious records. The third is partial completion. Use idempotency, reconciliation, checkpoints, and explicit compensation rather than an unbounded retry loop. The fourth is observability failure: a dashboard shows tokens but not who was affected or why. Emit structured events with access control and retention.

The fifth failure is metric gaming. A system can improve acceptance by refusing difficult requests, or improve latency by dropping evidence and safety checks. Define a minimum quality and safety floor before optimizing throughput. For human review, measure disagreement and overturns; a queue with 99% approvals may indicate excellent proposals or rubber-stamping. For privacy, avoid collecting raw content merely because it might be useful later.

The February source also has scope limits. OpenAI says Frontier is a platform to build, deploy, and manage agents; it describes shared context, onboarding, feedback, and explicit identity and permissions. The post reports, as customer examples, production optimization falling from six weeks to one day, more than 90% additional salesperson time, and output increasing by up to 5% at an energy producer. These are reported examples, not independently audited benchmarks. Nothing in that observation proves robustness against your adversaries, correctness on your domain, or a particular service-level target. Treat vendor examples as source facts and label recommendations as inference. When evidence is weak, abstention and escalation are valid outcomes.

## Evaluation and change management

Build a fixture set from ordinary, ambiguous, malformed, adversarial, slow, stale, and partially completed cases. Include a golden expected state and the invariants that must never break. Run the set against a pinned model and a deterministic baseline. Review failures by category, not just a total score. Keep hidden cases to detect overfitting, and sample production traces only after removing secrets.

Release gates should include a quality floor, a policy-violation ceiling, a reliability budget, a cost budget, and an evidence-completeness check. Roll out to a small cohort, compare with shadow results, and retain a kill switch that disables risky effects without destroying diagnostic reads. On rollback, record which version was disabled and whether external effects require remediation.

## February primary-source evidence

The source fact is bounded: **OpenAI says Frontier is a platform to build, deploy, and manage agents; it describes shared context, onboarding, feedback, and explicit identity and permissions. The post reports, as customer examples, production optimization falling from six weeks to one day, more than 90% additional salesperson time, and output increasing by up to 5% at an energy producer. These are reported examples, not independently audited benchmarks.** The February publication date and the publisher's wording should be cited when teaching the event. The recommendation that teams implement agent registry, semantic context layer, adapter, tenant control plane, and audit stream is an inference from the event plus established systems practice. It should be validated with local fixtures, security review, operational metrics, and domain experts. The source does not independently verify the examples, and this article does not present them as guarantees.

## Mini exercise extension

Create six fixtures for **root-cause investigation for a hardware manufacturer**: a normal request, missing evidence, an adversarial instruction, a policy denial, a timeout or interrupted run, and a successful outcome. For each fixture record the expected state, the allowed effect, and the evidence a reviewer should see. Add one version change and prove that the old event retains its original version. Your acceptance criterion is not a polished answer; it is a correct boundary, an explainable decision, and a safe recovery path.

## Build it locally: numbered implementation

1. Define dataclasses for `Request`, `Context`, `Proposal`, `Decision`, `Event`, and `Outcome`; require a run ID and version fields.
2. Write a deterministic boundary function for **agent registry, semantic context layer, adapter, tenant control plane, and audit stream**; deny unknown actions and malformed arguments.
3. Add a fake model that returns one valid and two invalid proposals, including an instruction hidden in retrieved text.
4. Add a fake downstream service with a timeout, an idempotency map, and a read-after-write reconciliation method.
5. Persist redacted JSON Lines events and implement replay without invoking a live model.
6. Run the six fixtures, assert the security invariant, and calculate tenant isolation errors, time to onboard a tool, useful completion rate, policy-denial rate, and cost per completed business outcome.
7. Change one policy or schema version, rerun the fixtures, and inspect the diff in evidence and state transitions.

## Runnable low-cost example

```python
from dataclasses import dataclass
@dataclass
class Agent:
    name: str
    tenant: str
    tools: frozenset

registry = {"support-acme": Agent("support-acme", "acme", frozenset({"search", "draft"}))}
request = ("support-acme", "acme", "delete")
a = registry.get(request[0])
print("allow" if a and a.tenant == request[1] and request[2] in a.tools else "deny")
```

This example is intentionally small and deterministic. It demonstrates the lesson's boundary and its invariant; it does not claim production-grade authentication, durability, isolation, or domain correctness. Extend it with the numbered build steps and failure fixtures before drawing operational conclusions.

## Interview Q&A

**Q: What is the difference between a source fact and an engineering inference?** A: The fact is what a dated publisher says it released, measured, or observed. The inference is a design recommendation derived from that fact and other knowledge; it needs local validation.

**Q: Why separate model output from the boundary?** A: Model output is probabilistic and can be manipulated by input. The boundary is deterministic, attributable code that can enforce authorization, schemas, budgets, and state transitions.

**Q: Which metric would you put on the dashboard first?** A: A useful outcome metric plus a failure metric specific to the topic—tenant isolation errors, time to onboard a tool, useful completion rate, policy-denial rate, and cost per completed business outcome. Pair it with slices so an aggregate cannot hide a critical regression.

**Q: When should the system abstain?** A: When evidence is missing or stale, the policy is ambiguous, the budget is exhausted, or an external effect has an unknown status. Escalate with evidence instead of fabricating confidence.

**Q: What should happen during rollout?** A: Pin versions, start in shadow or canary mode, limit high-risk effects, monitor quality/reliability/safety separately, and keep an audited rollback path.

## Glossary

- **Agent Registry**: the topic-specific control boundary that mediates a model proposal and an outcome.
- **Run ID**: a stable identifier joining request, context, decisions, attempts, and effects.
- **Idempotency**: repeating a request produces one logical effect rather than duplicates.
- **Provenance**: evidence describing origin, version, and transformations.
- **SLO**: a measurable service target such as latency or successful completion.
- **Abstention**: an explicit refusal or escalation when evidence or authority is insufficient.
- **Inference**: an engineering conclusion drawn from facts, not a quotation or guarantee from a source.

## References

- [OpenAI Frontier — February 5, 2026](https://openai.com/index/introducing-openai-frontier/)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)

## Claim ledger

| Claim | Source | Fact or inference |
|---|---|---|
| The cited publisher published the February event on the stated date. | [OpenAI Frontier, published February 5, 2026](https://openai.com/index/introducing-openai-frontier/) | Fact |
| OpenAI says Frontier is a platform to build, deploy, and manage agents; it describes shared context, onboarding, feedback, and explicit identity and permissions. | [OpenAI Frontier, published February 5, 2026](https://openai.com/index/introducing-openai-frontier/) | Fact |
| Turning a collection of clever pilots into a governed internal platform. | Engineering design synthesis | Inference |
| A separately enforced boundary is safer and easier to operate than treating model text as authority. | Topic standards and systems reasoning | Inference |
| The local example demonstrates the concept but does not prove production security, reliability, or generalization. | This lesson | Fact about the example |
