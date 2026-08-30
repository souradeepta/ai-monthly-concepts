# Content provenance
Status: durable
Sources: [W3C PROV — recommendation](https://www.w3.org/TR/prov-overview/); [C2PA — specification](https://c2pa.org/specifications/); [OpenAI's February 25, 2026 report, Disrupting malicious uses of AI](https://openai.com/index/disrupting-malicious-ai-uses/)
## In one sentence
Provenance records where content came from, which version transformed it, and who controls relevant rights.
## Background: what existed before
Files circulated detached from source, model, prompt, or edit history.
## What changed and why now
Generated and transformed content makes metadata and verifiable assertions operationally important.
## Impact on current processing and architecture
Carry source IDs, hashes, transforms, timestamps, and signatures through ingestion and export.
## Real-world applications and constraints
Useful in journalism and training-data review. Metadata stripping, key management, and partial adoption limit coverage.
## Mental model
```mermaid
flowchart LR
 S[Source]-->H[Hash]-->T[Transform]-->Sig[Signature]-->O[Output]
 classDef a fill:#dbeafe,stroke:#2563eb,color:#111827; classDef b fill:#dcfce7,stroke:#16a34a,color:#111827; class S,O a; class H,T,Sig b
```
```mermaid
sequenceDiagram
 Ingest->>Registry: source + hash
 Registry-->>Pipeline: provenance ID
 Pipeline->>Signer: output + manifest
 Signer-->>Consumer: signed assertion
```
## What changed this month
February treats provenance as a processing field, not a UI badge.
## Engineering consequence
Make provenance append-only where possible and verify signatures before trust decisions.
## Limits and failure modes
Valid provenance does not prove factual correctness; unsigned legacy content remains ambiguous.

## SDE2 primer and prerequisites

This lesson is about **content provenance** as a production systems problem. A language model is only one stage: an ingress service accepts work, a data layer supplies evidence, an orchestrator keeps state, a policy layer decides what may happen, and an operator or downstream system observes the result. Students should know HTTP, JSON, functions, and basic databases. SDE2 readers should also know queues, authentication, structured logs, metrics, retries, and service-level objectives (SLOs). The central habit is to label what the February source actually reports separately from a recommendation derived from it.

The useful boundary for content provenance is **lineage, content hash, transformation manifest, signer, assertion, chain of custody, and verification**. These are not magic model capabilities. They are interfaces, records, checks, and operating procedures that can be unit-tested. Start with a low-blast-radius workflow and make every external effect attributable to a run ID, actor, policy version, and evidence reference.

## February source reading: fact before inference

The primary February event is **OpenAI's February 25, 2026 report, Disrupting malicious uses of AI**. OpenAI's February report emphasizes that malicious activity can cross AI models, platforms, websites, and social accounts. That makes evidence continuity a timely operational problem, but the report does not endorse C2PA or W3C PROV. Those standards provide a vocabulary for implementing the inference that investigators need a machine-readable history. The report or announcement is evidence about what its publisher described. It is not independent validation of the publisher's claims, and it does not specify your data, threat model, latency budget, or regulatory obligations. That distinction matters because a source can motivate a concept without proving that the concept is solved.

The engineering inference in this lesson is that carrying verifiable history through ingestion, model transformation, export, and investigation. Write that inference as a testable contract: state the accepted inputs, expected transitions, forbidden outcomes, and evidence needed to review a decision. If a test fails, improve the system or narrow the intended use; do not silently reinterpret a source claim as a guarantee.

## Historical baseline and problem boundary

Before this month's event, a team could make a convincing prototype with a synchronous request, a prompt, one model call, and a small script around an API. That baseline remains appropriate for drafting or a read-only experiment. It becomes unsafe or unreliable when a request crosses systems, waits, changes durable data, or must be explained later. The failure is not merely that the model can be wrong. It is that the surrounding software may have no place to record authority, version, evidence, retries, or recourse.

For **preserving the origin and edits of an image or report used in an incident review**, draw the boundary before choosing a model. Identify the human or service principal, the records allowed into context, the actions proposed by the model, the component that validates them, and the owner who handles an ambiguous result. Decide which operations are reads, reversible writes, irreversible writes, or merely recommendations. A useful rule is that an untrusted string may influence a proposal but may never create a permission, erase an audit event, or bypass a state transition.

## Architecture and data flow

A deployable design has a control path and a data path. The control path versions configuration, policy, model adapters, schemas, evaluation sets, and rollout cohorts. The data path receives a request, authenticates it, retrieves bounded evidence, invokes the model, validates a typed proposal, executes an allowed action, and records an outcome. The content provenance boundary sits between the proposal and the observable outcome; it should be visible in traces and owned by a team.

```mermaid
flowchart LR
  A[Caller] --> I[Identity and tenant]
  I --> C[Context/evidence]
  C --> M[Model proposal]
  M --> B[Lineage boundary]
  B --> X[Effect or review]
  X --> L[(Evidence log)]
  classDef data fill:#dbeafe,stroke:#2563eb,color:#172554; classDef control fill:#dcfce7,stroke:#15803d,color:#14532d; classDef risk fill:#fee2e2,stroke:#dc2626,color:#450a0a
  class A,C,X,L data; class I,B control; class M risk
```

Use separate fields for user text, retrieved facts, policy instructions, tool output, and generated proposal. This prevents an instruction hidden in a document or tool result from acquiring the authority of a system rule. Every record should carry a tenant or project key where relevant. Cache keys must include authorization scope and source version. Logs should retain enough structured evidence to explain a decision while redacting secrets and unnecessary free text.

A minimal run record is: `run_id`, `request_id`, actor, tenant, purpose, model/version, policy/version, context references, proposal hash, action, decision, timestamps, attempts, effect IDs, and final status. For this topic add lineage, content hash, transformation manifest, signer, assertion, chain of custody, and verification. Do not put an unbounded transcript in the primary operational table; store a redacted pointer with a retention policy.

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

Persist the proposal before a side effect. On retry, reuse the same idempotency key or proof artifact rather than asking the model to invent a new action. A timeout is a state of knowledge, not proof that nothing happened. For a reversible operation, record the compensating action; for an irreversible operation, stop and escalate. For this lesson, the most important transition is the one that prevents **preserving the origin and edits of an image or report used in an incident review** from becoming an unreviewed or untraceable effect.

## Topic mechanics: Content provenance

### Decision model and topic-specific data contract

A provenance record is a graph of entities and transformations, not a decorative badge. On ingest, hash the bytes, record source URI and acquisition time, and assign an asset ID. Each model or human transform consumes one or more assets and emits a new asset with tool version, parameters, operator or service identity, and output hash. A signed assertion authenticates who made a statement about the graph; it does not prove that the content is true. C2PA can carry creator and edit assertions, while W3C PROV supplies a general entity/activity/agent vocabulary. For an incident image, preserve the original, a normalized copy, an OCR result, a model summary, and every export as separate nodes. Verify signatures and hashes before using provenance in a trust or ranking decision. Metadata stripping and screenshots create gaps; represent “unknown” rather than inventing lineage. Key rotation, offline verification, and legacy unsigned content need explicit policy. The February malicious-use report makes this relevant because evidence can cross platforms and models; it does not itself prescribe a provenance standard. Measure reconstruction time and missing-link rate, not the number of badges displayed.

The first implementation question is what the system can know at each stage. At ingress, it knows an authenticated actor and a request, but not whether the request is well-formed or authorized. During retrieval, it can establish source IDs, freshness, and access filters, but similarity is not truth. During model generation, it can ask for a schema and bounded plan, but the output is still untrusted. At the boundary, deterministic code can enforce limits. After execution, only a receipt, read-after-write check, or independent artifact establishes what happened. This epistemic separation keeps **lineage, content hash, transformation manifest, signer, assertion, chain of custody, and verification** from collapsing into one prompt.

The second question is what must be versioned. Version the schema, policy, model adapter, context query, evaluator, and relevant data snapshot. Include the version in the run record and in emitted events. A deployment that changes a prompt but cannot identify which runs saw it cannot explain a regression. A policy change must not rewrite history: old runs retain the decision and policy that actually governed them.

The third question is where to put backpressure. Limit model calls, tool calls, context size, queue age, reviewer workload, and cumulative cost. Admission control should happen before expensive retrieval or inference when the request cannot meet its deadline or safety requirements. A bounded budget also makes failure legible: `budget_exhausted` is different from `model_error`, `policy_denied`, or `unknown_commit`.

For **content provenance**, instrument verified-asset rate, missing-manifest rate, hash mismatches, signer-key failures, and time to reconstruct lineage. Break down every metric by task slice, tenant, model version, policy version, and outcome class. An aggregate success number can improve while a small high-risk slice becomes worse. Pair capability metrics with reliability metrics and safety metrics; never use one as a proxy for the others.


## Content provenance: focused design workshop

The distinctive design choice for this lesson is **lineage graphs and signed assertions**. Model the core record as a typed object with `asset_id, parent_hash, transform, signer, output_hash`. Keep user prose outside that object; prose can explain intent, but code must decide whether the object is complete, authorized, fresh, and safe to execute. The invariant is: **a valid signature authenticates an assertion but does not prove truth**. Emit an event whenever the invariant is checked, including the result, version, actor, and evidence reference. This makes a failure diagnosable without replaying an unconstrained model call.

Consider a concrete **content provenance** run. The ingress validator rejects missing identifiers and normalizes timestamps. The context builder retrieves only records permitted by tenant and purpose. The model receives a bounded view and returns a proposal, never a bearer credential or an opaque instruction. The topic-specific boundary then checks `asset_id, parent_hash, transform, signer, output_hash`. If the check passes, the effect owner commits or queues work and returns a receipt. If it fails, the system returns a structured denial or asks for evidence. A reviewer can inspect the event sequence and distinguish bad input, missing authority, stale state, and a remote failure.

There are two subtle cases worth testing. First, a valid record can become invalid between proposal and commit: an approval can expire, a memory can be deleted, a benchmark can be rerun with a different evaluator, or a capacity pool can fill. Recheck the relevant version at the boundary. Second, an invalid record can look plausible because a model or a dashboard smooths away uncertainty. Preserve `unknown`, `abstain`, and `needs_review` as first-class outcomes. Never convert them to success to simplify reporting.

For operations, partition metrics by `lineage graphs and signed assertions` and by model, policy, tenant, and outcome. Track the invariant violation directly, plus useful completion, latency, cost, and human override. A single aggregate can hide a catastrophic slice: one customer, one high-risk action, one rare theorem class, or one overloaded region. Set a release floor for the topic-specific safety metric before optimizing throughput.

The mini design exercise is **detect a changed image and represent missing legacy metadata as unknown**. Implement it with an in-memory store first, then add a failure injection at every boundary. Expected behavior should be deterministic even if the proposal generator is not. Save the failing input as a regression fixture only after removing secrets and identifying the policy version that governed it.


## Applications and operational constraints

The strongest first application is **preserving the origin and edits of an image or report used in an incident review** because it has a bounded workflow and a domain owner. A team might begin in shadow mode, where the system produces a proposal but performs no effect. Next, allow a canary cohort and only low-risk actions. Require an explicit launch review before expanding scope. The useful outcome is not “the model answered”; it is a completed task that meets quality, latency, cost, privacy, and policy constraints.

Other plausible applications include journalism, incident response, synthetic-media review, training-data governance, and legal discovery. Each has a different bottleneck. A support system values queue age and consistent escalation; an operations system values correctness and rollback; research values evidence and uncertainty; security values time to detect and false-positive capacity. Data residency, tenant isolation, secrets, rate limits, procurement, and human availability can dominate model latency. Document those constraints in the service contract rather than in an informal prompt.

Capacity planning should include the non-model dependencies. Retrieval may saturate a database, reviewers may saturate a queue, a policy service may add p95 latency, and a downstream API may have a stricter quota than the model. Budget the entire critical path and provide a degraded mode: read-only output, draft-only output, cached evidence, or a human handoff. A degraded response must be labeled so a user does not mistake it for a normal completion.

## Failure modes, security, and limits

The first failure mode is authority confusion: a generated plan is treated as a decision. Enforce the boundary in the effect-owning service and test adversarial proposals. The second is stale or poisoned context. Attach provenance and freshness, isolate tenants, and quarantine suspicious records. The third is partial completion. Use idempotency, reconciliation, checkpoints, and explicit compensation rather than an unbounded retry loop. The fourth is observability failure: a dashboard shows tokens but not who was affected or why. Emit structured events with access control and retention.

The fifth failure is metric gaming. A system can improve acceptance by refusing difficult requests, or improve latency by dropping evidence and safety checks. Define a minimum quality and safety floor before optimizing throughput. For human review, measure disagreement and overturns; a queue with 99% approvals may indicate excellent proposals or rubber-stamping. For privacy, avoid collecting raw content merely because it might be useful later.

The February source also has scope limits. OpenAI's February report emphasizes that malicious activity can cross AI models, platforms, websites, and social accounts. That makes evidence continuity a timely operational problem, but the report does not endorse C2PA or W3C PROV. Those standards provide a vocabulary for implementing the inference that investigators need a machine-readable history. Nothing in that observation proves robustness against your adversaries, correctness on your domain, or a particular service-level target. Treat vendor examples as source facts and label recommendations as inference. When evidence is weak, abstention and escalation are valid outcomes.

## Evaluation and change management

Build a fixture set from ordinary, ambiguous, malformed, adversarial, slow, stale, and partially completed cases. Include a golden expected state and the invariants that must never break. Run the set against a pinned model and a deterministic baseline. Review failures by category, not just a total score. Keep hidden cases to detect overfitting, and sample production traces only after removing secrets.

Release gates should include a quality floor, a policy-violation ceiling, a reliability budget, a cost budget, and an evidence-completeness check. Roll out to a small cohort, compare with shadow results, and retain a kill switch that disables risky effects without destroying diagnostic reads. On rollback, record which version was disabled and whether external effects require remediation.

## February primary-source evidence

The source fact is bounded: **OpenAI's February report emphasizes that malicious activity can cross AI models, platforms, websites, and social accounts. That makes evidence continuity a timely operational problem, but the report does not endorse C2PA or W3C PROV. Those standards provide a vocabulary for implementing the inference that investigators need a machine-readable history.** The February publication date and the publisher's wording should be cited when teaching the event. The recommendation that teams implement lineage, content hash, transformation manifest, signer, assertion, chain of custody, and verification is an inference from the event plus established systems practice. It should be validated with local fixtures, security review, operational metrics, and domain experts. The source does not independently verify the examples, and this article does not present them as guarantees.

## Mini exercise extension

Create six fixtures for **preserving the origin and edits of an image or report used in an incident review**: a normal request, missing evidence, an adversarial instruction, a policy denial, a timeout or interrupted run, and a successful outcome. For each fixture record the expected state, the allowed effect, and the evidence a reviewer should see. Add one version change and prove that the old event retains its original version. Your acceptance criterion is not a polished answer; it is a correct boundary, an explainable decision, and a safe recovery path.

## Build it locally: numbered implementation

1. Define dataclasses for `Request`, `Context`, `Proposal`, `Decision`, `Event`, and `Outcome`; require a run ID and version fields.
2. Write a deterministic boundary function for **lineage, content hash, transformation manifest, signer, assertion, chain of custody, and verification**; deny unknown actions and malformed arguments.
3. Add a fake model that returns one valid and two invalid proposals, including an instruction hidden in retrieved text.
4. Add a fake downstream service with a timeout, an idempotency map, and a read-after-write reconciliation method.
5. Persist redacted JSON Lines events and implement replay without invoking a live model.
6. Run the six fixtures, assert the security invariant, and calculate verified-asset rate, missing-manifest rate, hash mismatches, signer-key failures, and time to reconstruct lineage.
7. Change one policy or schema version, rerun the fixtures, and inspect the diff in evidence and state transitions.

## Runnable low-cost example

```python
import hashlib
def digest(data): return hashlib.sha256(data.encode()).hexdigest()
source = digest("original image")
output = digest("cropped image")
manifest = {"asset":"out-1", "parent":source, "output":output, "transform":"crop-v2"}
print(manifest["parent"] == digest("original image"))
```

This example is intentionally small and deterministic. It demonstrates the lesson's boundary and its invariant; it does not claim production-grade authentication, durability, isolation, or domain correctness. Extend it with the numbered build steps and failure fixtures before drawing operational conclusions.

## Interview Q&A

**Q: What is the difference between a source fact and an engineering inference?** A: The fact is what a dated publisher says it released, measured, or observed. The inference is a design recommendation derived from that fact and other knowledge; it needs local validation.

**Q: Why separate model output from the boundary?** A: Model output is probabilistic and can be manipulated by input. The boundary is deterministic, attributable code that can enforce authorization, schemas, budgets, and state transitions.

**Q: Which metric would you put on the dashboard first?** A: A useful outcome metric plus a failure metric specific to the topic—verified-asset rate, missing-manifest rate, hash mismatches, signer-key failures, and time to reconstruct lineage. Pair it with slices so an aggregate cannot hide a critical regression.

**Q: When should the system abstain?** A: When evidence is missing or stale, the policy is ambiguous, the budget is exhausted, or an external effect has an unknown status. Escalate with evidence instead of fabricating confidence.

**Q: What should happen during rollout?** A: Pin versions, start in shadow or canary mode, limit high-risk effects, monitor quality/reliability/safety separately, and keep an audited rollback path.

## Glossary

- **Lineage**: the topic-specific control boundary that mediates a model proposal and an outcome.
- **Run ID**: a stable identifier joining request, context, decisions, attempts, and effects.
- **Idempotency**: repeating a request produces one logical effect rather than duplicates.
- **Provenance**: evidence describing origin, version, and transformations.
- **SLO**: a measurable service target such as latency or successful completion.
- **Abstention**: an explicit refusal or escalation when evidence or authority is insufficient.
- **Inference**: an engineering conclusion drawn from facts, not a quotation or guarantee from a source.

## References

- [OpenAI: Disrupting malicious uses of AI — February 25, 2026](https://openai.com/index/disrupting-malicious-ai-uses/)
- [W3C PROV overview](https://www.w3.org/TR/prov-overview/)
- [C2PA specifications](https://c2pa.org/specifications/)

## Claim ledger

| Claim | Source | Fact or inference |
|---|---|---|
| The cited publisher published the February event on the stated date. | [OpenAI's February 25, 2026 report, Disrupting malicious uses of AI](https://openai.com/index/disrupting-malicious-ai-uses/) | Fact |
| OpenAI's February report emphasizes that malicious activity can cross AI models, platforms, websites, and social accounts. | [OpenAI's February 25, 2026 report, Disrupting malicious uses of AI](https://openai.com/index/disrupting-malicious-ai-uses/) | Fact |
| Carrying verifiable history through ingestion, model transformation, export, and investigation. | Engineering design synthesis | Inference |
| A separately enforced boundary is safer and easier to operate than treating model text as authority. | Topic standards and systems reasoning | Inference |
| The local example demonstrates the concept but does not prove production security, reliability, or generalization. | This lesson | Fact about the example |
