# Approval workflows
Status: durable
Sources: [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework); [OpenAI — 2026-02-05](https://openai.com/index/introducing-openai-frontier/)
## In one sentence
Approval workflows pause consequential actions until an accountable human reviews evidence and scope.
## Background: what existed before
Automation often optimized completion and treated review as an informal afterthought.
## What changed and why now
Agent plans can cross irreversible boundaries, so review becomes a state transition with auditability.
## Impact on current processing and architecture
Separate propose, review, approve, execute, and reconcile states; show diffs rather than raw prompts.
## Real-world applications and constraints
Use for refunds and production changes. Reviewer fatigue, latency, and rubber-stamping limit effectiveness.
## Mental model
```mermaid
flowchart LR
 P[Propose]-->H[Human review]-->A[Approve]-->E[Execute]-->R[Reconcile]
 classDef a fill:#dbeafe,stroke:#2563eb,color:#111827; classDef b fill:#fef3c7,stroke:#d97706,color:#111827; class P,E,R a; class H,A b
```
```mermaid
stateDiagram-v2
 Draft --> Pending
 Pending --> Approved
 Pending --> Rejected
 Approved --> Executed
 Executed --> Reconciled
```
## What changed this month
February positions approval as a control-plane primitive for agents.
## Engineering consequence
Make approvals scoped, expiring, attributable, and bound to an immutable action hash.
## Limits and failure modes
A reviewer can approve incomplete evidence; stale approvals and UI spoofing remain risks.

## SDE2 primer and prerequisites

This lesson is about **approval workflows** as a production systems problem. A language model is only one stage: an ingress service accepts work, a data layer supplies evidence, an orchestrator keeps state, a policy layer decides what may happen, and an operator or downstream system observes the result. Students should know HTTP, JSON, functions, and basic databases. SDE2 readers should also know queues, authentication, structured logs, metrics, retries, and service-level objectives (SLOs). The central habit is to label what the February source actually reports separately from a recommendation derived from it.

The useful boundary for approval workflows is **approval intent, reviewer assignment, separation of duties, expiry, evidence packet, and escalation**. These are not magic model capabilities. They are interfaces, records, checks, and operating procedures that can be unit-tested. Start with a low-blast-radius workflow and make every external effect attributable to a run ID, actor, policy version, and evidence reference.

## February source reading: fact before inference

The primary February event is **OpenAI Frontier, published February 5, 2026**. Frontier says AI coworkers should have clear permissions and boundaries and should improve quality through feedback. Those statements support an approval boundary as an engineering interpretation. NIST risk-management practice supplies the governance vocabulary; neither source says that a human click automatically makes an action safe. The report or announcement is evidence about what its publisher described. It is not independent validation of the publisher's claims, and it does not specify your data, threat model, latency budget, or regulatory obligations. That distinction matters because a source can motivate a concept without proving that the concept is solved.

The engineering inference in this lesson is that making a human decision a durable, attributable state transition rather than a button in a chat UI. Write that inference as a testable contract: state the accepted inputs, expected transitions, forbidden outcomes, and evidence needed to review a decision. If a test fails, improve the system or narrow the intended use; do not silently reinterpret a source claim as a guarantee.

## Historical baseline and problem boundary

Before this month's event, a team could make a convincing prototype with a synchronous request, a prompt, one model call, and a small script around an API. That baseline remains appropriate for drafting or a read-only experiment. It becomes unsafe or unreliable when a request crosses systems, waits, changes durable data, or must be explained later. The failure is not merely that the model can be wrong. It is that the surrounding software may have no place to record authority, version, evidence, retries, or recourse.

For **an agent preparing a vendor payment or production change for a named human approver**, draw the boundary before choosing a model. Identify the human or service principal, the records allowed into context, the actions proposed by the model, the component that validates them, and the owner who handles an ambiguous result. Decide which operations are reads, reversible writes, irreversible writes, or merely recommendations. A useful rule is that an untrusted string may influence a proposal but may never create a permission, erase an audit event, or bypass a state transition.

## Architecture and data flow

A deployable design has a control path and a data path. The control path versions configuration, policy, model adapters, schemas, evaluation sets, and rollout cohorts. The data path receives a request, authenticates it, retrieves bounded evidence, invokes the model, validates a typed proposal, executes an allowed action, and records an outcome. The approval workflows boundary sits between the proposal and the observable outcome; it should be visible in traces and owned by a team.

```mermaid
flowchart LR
  A[Caller] --> I[Identity and tenant]
  I --> C[Context/evidence]
  C --> M[Model proposal]
  M --> B[Approval Intent boundary]
  B --> X[Effect or review]
  X --> L[(Evidence log)]
  classDef data fill:#dbeafe,stroke:#2563eb,color:#172554; classDef control fill:#dcfce7,stroke:#15803d,color:#14532d; classDef risk fill:#fee2e2,stroke:#dc2626,color:#450a0a
  class A,C,X,L data; class I,B control; class M risk
```

Use separate fields for user text, retrieved facts, policy instructions, tool output, and generated proposal. This prevents an instruction hidden in a document or tool result from acquiring the authority of a system rule. Every record should carry a tenant or project key where relevant. Cache keys must include authorization scope and source version. Logs should retain enough structured evidence to explain a decision while redacting secrets and unnecessary free text.

A minimal run record is: `run_id`, `request_id`, actor, tenant, purpose, model/version, policy/version, context references, proposal hash, action, decision, timestamps, attempts, effect IDs, and final status. For this topic add approval intent, reviewer assignment, separation of duties, expiry, evidence packet, and escalation. Do not put an unbounded transcript in the primary operational table; store a redacted pointer with a retention policy.

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

Persist the proposal before a side effect. On retry, reuse the same idempotency key or proof artifact rather than asking the model to invent a new action. A timeout is a state of knowledge, not proof that nothing happened. For a reversible operation, record the compensating action; for an irreversible operation, stop and escalate. For this lesson, the most important transition is the one that prevents **an agent preparing a vendor payment or production change for a named human approver** from becoming an unreviewed or untraceable effect.

## Topic mechanics: Approval workflows

### Decision model and topic-specific data contract

An approval is a state transition with identity and evidence. Create an approval intent containing the proposed action, exact arguments, affected resources, risk classification, evidence links, policy version, expiry, and required reviewer role. The reviewer should see a stable snapshot or a version conflict, not a live amount that can change after clicking. Separation of duties prevents the proposer or an automated worker from approving its own high-risk action. Expire approvals when context, price, permission, or risk changes. If two reviewers are required, store both decisions and the quorum rule. Execute only after a final authorization check and bind the effect ID to the approval ID. For vendor payments, display amount, currency, vendor, invoice evidence, and rollback options; an opaque “approve agent plan” button is not meaningful consent. Test replayed approvals, approval phishing, stale evidence, reviewer unavailability, and a race where a user revokes access while a job is queued. Measure disagreement and overturns, not just time-to-click. Frontier's boundaries and feedback framing support the idea of governed work; NIST provides risk-management language, while the workflow mechanics are this lesson's inference.

The first implementation question is what the system can know at each stage. At ingress, it knows an authenticated actor and a request, but not whether the request is well-formed or authorized. During retrieval, it can establish source IDs, freshness, and access filters, but similarity is not truth. During model generation, it can ask for a schema and bounded plan, but the output is still untrusted. At the boundary, deterministic code can enforce limits. After execution, only a receipt, read-after-write check, or independent artifact establishes what happened. This epistemic separation keeps **approval intent, reviewer assignment, separation of duties, expiry, evidence packet, and escalation** from collapsing into one prompt.

Approval workflows should version the proposal schema, approver matrix, evidence requirements, expiry interval, and escalation route. Bind those versions to the approval token; a policy update must invalidate or re-review affected proposals without erasing the original decision context.

Approval queues need limits on case age, evidence size, reassignment count, and approver workload. If a case cannot meet its expiry window, defer it before collecting more model output. Distinguish `awaiting_approver`, `evidence_incomplete`, and `approval_expired`; each needs a different human action.

For **approval workflows**, instrument review latency, approval disagreement, stale-approval rate, bypass attempts, and effect-to-approval linkage. Break down every metric by task slice, tenant, model version, policy version, and outcome class. An aggregate success number can improve while a small high-risk slice becomes worse. Pair capability metrics with reliability metrics and safety metrics; never use one as a proxy for the others.


## Approval workflows: focused design workshop

The distinctive design choice for this lesson is **approval intents and separation of duties**. Model the core record as a typed object with `approval_id, proposer, reviewer, payload_hash, expires_at`. Keep user prose outside that object; prose can explain intent, but code must decide whether the object is complete, authorized, fresh, and safe to execute. The invariant is: **only the named role can approve the unchanged evidence snapshot**. Emit an event whenever the invariant is checked, including the result, version, actor, and evidence reference. This makes a failure diagnosable without replaying an unconstrained model call.

Consider a concrete **approval workflows** run. The ingress validator rejects missing identifiers and normalizes timestamps. The context builder retrieves only records permitted by tenant and purpose. The model receives a bounded view and returns a proposal, never a bearer credential or an opaque instruction. The topic-specific boundary then checks `approval_id, proposer, reviewer, payload_hash, expires_at`. If the check passes, the effect owner commits or queues work and returns a receipt. If it fails, the system returns a structured denial or asks for evidence. A reviewer can inspect the event sequence and distinguish bad input, missing authority, stale state, and a remote failure.

Test approval races. An approver can lose authority after clicking approve, or the underlying amount and evidence can change before execution. Bind approval to proposal digest, actor, scope, and expiry, then recheck all four at the action gate. Preserve `approval_expired` and `proposal_changed`; neither means approved.

For operations, partition metrics by `approval intents and separation of duties` and by model, policy, tenant, and outcome. Track the invariant violation directly, plus useful completion, latency, cost, and human override. A single aggregate can hide a catastrophic slice: one customer, one high-risk action, one rare theorem class, or one overloaded region. Set a release floor for the topic-specific safety metric before optimizing throughput.

The mini design exercise is **reject a replayed approval after its invoice hash changes**. Implement it with an in-memory store first, then add a failure injection at every boundary. Expected behavior should be deterministic even if the proposal generator is not. Save the failing input as a regression fixture only after removing secrets and identifying the policy version that governed it.


## Applications and operational constraints

The strongest first application is **an agent preparing a vendor payment or production change for a named human approver** because it has a bounded workflow and a domain owner. A team might begin in shadow mode, where the system produces a proposal but performs no effect. Next, allow a canary cohort and only low-risk actions. Require an explicit launch review before expanding scope. The useful outcome is not “the model answered”; it is a completed task that meets quality, latency, cost, privacy, and policy constraints.

Other plausible applications include payments, access requests, medical administration, publishing, and production operations. Each has a different bottleneck. A support system values queue age and consistent escalation; an operations system values correctness and rollback; research values evidence and uncertainty; security values time to detect and false-positive capacity. Data residency, tenant isolation, secrets, rate limits, procurement, and human availability can dominate model latency. Document those constraints in the service contract rather than in an informal prompt.

Plan approval capacity around approver coverage, evidence assembly, escalations, and appeal handling. A full queue should trigger safe deferral, not lower the review threshold. Tell the requester whether a proposal is awaiting a person, missing evidence, or expired rather than presenting a delayed case as approved.

## Failure modes, security, and limits

Approval failures include rubber-stamping, missing evidence, stale approvals, and queue starvation for high-risk cases. Show approvers the exact proposed effect and its evidence, bind approval to a digest and expiry, and reauthorize immediately before execution. Measure overturns and safe deferrals, not just approval percentage.

Approval metrics can improve by routing difficult cases away, shortening review, or treating every click as informed consent. Pair approval time with evidence completeness, overturns, appeals, and post-action incidents. A near-perfect approval rate may reveal rubber-stamping rather than excellent proposals.

The February source also has scope limits. Frontier says AI coworkers should have clear permissions and boundaries and should improve quality through feedback. Those statements support an approval boundary as an engineering interpretation. NIST risk-management practice supplies the governance vocabulary; neither source says that a human click automatically makes an action safe. Nothing in that observation proves robustness against your adversaries, correctness on your domain, or a particular service-level target. Treat vendor examples as source facts and label recommendations as inference. When evidence is weak, abstention and escalation are valid outcomes.

## Evaluation and change management

Build a fixture set from ordinary, ambiguous, malformed, adversarial, slow, stale, and partially completed cases. Include a golden expected state and the invariants that must never break. Run the set against a pinned model and a deterministic baseline. Review failures by category, not just a total score. Keep hidden cases to detect overfitting, and sample production traces only after removing secrets.

Release gates should include a quality floor, a policy-violation ceiling, a reliability budget, a cost budget, and an evidence-completeness check. Roll out to a small cohort, compare with shadow results, and retain a kill switch that disables risky effects without destroying diagnostic reads. On rollback, record which version was disabled and whether external effects require remediation.

## February primary-source evidence

The source fact is bounded: **Frontier says AI coworkers should have clear permissions and boundaries and should improve quality through feedback. Those statements support an approval boundary as an engineering interpretation. NIST risk-management practice supplies the governance vocabulary; neither source says that a human click automatically makes an action safe.** The February publication date and the publisher's wording should be cited when teaching the event. The recommendation that teams implement approval intent, reviewer assignment, separation of duties, expiry, evidence packet, and escalation is an inference from the event plus established systems practice. It should be validated with local fixtures, security review, operational metrics, and domain experts. The source does not independently verify the examples, and this article does not present them as guarantees.

## Mini exercise extension

Create six fixtures for **an agent preparing a vendor payment or production change for a named human approver**: a normal request, missing evidence, an adversarial instruction, a policy denial, a timeout or interrupted run, and a successful outcome. For each fixture record the expected state, the allowed effect, and the evidence a reviewer should see. Add one version change and prove that the old event retains its original version. Your acceptance criterion is not a polished answer; it is a correct boundary, an explainable decision, and a safe recovery path.

## Build it locally: numbered implementation

1. Define dataclasses for `Request`, `Context`, `Proposal`, `Decision`, `Event`, and `Outcome`; require a run ID and version fields.
2. Write a deterministic boundary function for **approval intent, reviewer assignment, separation of duties, expiry, evidence packet, and escalation**; deny unknown actions and malformed arguments.
3. Add a fake model that returns one valid and two invalid proposals, including an instruction hidden in retrieved text.
4. Add a fake downstream service with a timeout, an idempotency map, and a read-after-write reconciliation method.
5. Persist redacted JSON Lines events and implement replay without invoking a live model.
6. Run the six fixtures, assert the security invariant, and calculate review latency, approval disagreement, stale-approval rate, bypass attempts, and effect-to-approval linkage.
7. Change one policy or schema version, rerun the fixtures, and inspect the diff in evidence and state transitions.

## Runnable low-cost example

```python
import hashlib
def approval(payload, reviewer, expected):
    digest = hashlib.sha256(payload.encode()).hexdigest()
    return reviewer == "finance-manager" and digest == expected
payload = "invoice:42:900"
h = hashlib.sha256(payload.encode()).hexdigest()
print(approval(payload, "finance-manager", h), approval("invoice:42:1200", "finance-manager", h))
```

This example is intentionally small and deterministic. It demonstrates the lesson's boundary and its invariant; it does not claim production-grade authentication, durability, isolation, or domain correctness. Extend it with the numbered build steps and failure fixtures before drawing operational conclusions.

## Interview Q&A

**Q: What is the difference between a source fact and an engineering inference?** A: The fact is what a dated publisher says it released, measured, or observed. The inference is a design recommendation derived from that fact and other knowledge; it needs local validation.

**Q: Why separate model output from the boundary?** A: Model output is probabilistic and can be manipulated by input. The boundary is deterministic, attributable code that can enforce authorization, schemas, budgets, and state transitions.

**Q: Which metric would you put on the dashboard first?** A: A useful outcome metric plus a failure metric specific to the topic—review latency, approval disagreement, stale-approval rate, bypass attempts, and effect-to-approval linkage. Pair it with slices so an aggregate cannot hide a critical regression.

**Q: When should the system abstain?** A: When evidence is missing or stale, the policy is ambiguous, the budget is exhausted, or an external effect has an unknown status. Escalate with evidence instead of fabricating confidence.

**Q: What should happen during rollout?** A: Pin versions, start in shadow or canary mode, limit high-risk effects, monitor quality/reliability/safety separately, and keep an audited rollback path.

## Glossary

- **Approval Intent**: the topic-specific control boundary that mediates a model proposal and an outcome.
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
| Frontier says AI coworkers should have clear permissions and boundaries and should improve quality through feedback. | [OpenAI Frontier, published February 5, 2026](https://openai.com/index/introducing-openai-frontier/) | Fact |
| Making a human decision a durable, attributable state transition rather than a button in a chat ui. | Engineering design synthesis | Inference |
| A separately enforced boundary is safer and easier to operate than treating model text as authority. | Topic standards and systems reasoning | Inference |
| The local example demonstrates the concept but does not prove production security, reliability, or generalization. | This lesson | Fact about the example |
