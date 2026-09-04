# Permission boundaries
Status: durable
Sources: [OWASP — LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/); [NIST zero trust](https://www.nist.gov/publications/zero-trust-architecture); [OpenAI Frontier, published February 5, 2026](https://openai.com/index/introducing-openai-frontier/)
## In one sentence
Model output proposes actions; a separately enforced policy decides whether those actions are permitted.
## Background: what existed before
Many prototypes passed generated SQL or URLs directly to privileged services.
## What changed and why now
Prompt injection and tool use exposed the need for defense in depth and explicit authorization.
## Impact on current processing and architecture
Put policy between model and side effect; validate arguments, tenant, actor, and approval state.
## Real-world applications and constraints
Email, payments, and database agents need deny-by-default controls. Policy latency and false denials affect UX.
## Mental model
```mermaid
flowchart LR
 M[Model proposal]-->V[Validator]-->P[Policy]-->A[Approval]-->E[Effect]
 classDef c fill:#dbeafe,stroke:#2563eb,color:#111827; classDef s fill:#fee2e2,stroke:#dc2626,color:#111827; class M,V,P,A c; class E s
```
```mermaid
sequenceDiagram
 Model->>Gateway: delete(record=7)
 Gateway->>Policy: subject + scope + resource
 Policy-->>Gateway: deny
 Gateway-->>Model: structured error
```
## What changed this month
February makes authorization an explicit boundary in agent architecture.
## Engineering consequence
Never infer access from text; use server-side allow-lists and immutable audit events.
## Limits and failure modes
Policy bugs, confused-deputy paths, and overly broad service accounts remain possible.

## SDE2 primer and prerequisites

This lesson treats **permission boundaries** as a resource-enforcement problem. The model can propose intent, but identity, policy, resource state, and the effect owner determine whether that intent becomes an action. Students should know HTTP, JSON, authentication, and basic databases. For SDE2 work, add capabilities, delegation, revocation, audit events, retries, and SLOs. Separate source facts from authorization guarantees that require local tests.

The useful boundary for permission boundaries is **policy decision point, capability token, resource predicate, row filter, deny default, and confused deputy**. These are not magic model capabilities. They are interfaces, records, checks, and operating procedures that can be unit-tested. Start with a low-blast-radius workflow and make every external effect attributable to a run ID, actor, policy version, and evidence reference.

## February source reading: fact before inference

For permission boundaries, read the February source through its own claim boundary. The cited February event is **OpenAI Frontier, published February 5, 2026**. Frontier says AI coworkers have explicit permissions and guardrails. The February fact is the product's stated boundary model; OWASP and zero-trust principles explain why a model proposal must still be checked by the service that owns the side effect. A prompt is not an authorization mechanism. The report or announcement is evidence about what its publisher described. It is not independent validation of the publisher's claims, and it does not specify your data, threat model, latency budget, or regulatory obligations. That distinction matters because a source can motivate a concept without proving that the concept is solved.

For permission boundaries, the engineering inference is narrower: turn the cited capability into an operational contract with topic-specific inputs, states, evidence, and failure ownership. Test that contract against ordinary, adversarial, stale, and interrupted work. A source can motivate this design; it cannot guarantee the resulting reliability or safety.

## Historical baseline and problem boundary

The useful permission baseline is an authenticated request checked once by an application gateway. That is inadequate when a model can choose tools, requests wait in queues, or resources change ownership. A permission boundary must be enforced again at the resource and effect owner with current scope.

For **permission boundaries**, the permission boundaries boundary names permission boundaries evidence, the actor, the mutable state, and the rejecting component. Treat read evidence, model proposals, and committed effects as different data classes. A request can influence a proposal but cannot grant authority. Test this boundary with stale, malformed, replayed, and partially completed cases.

## Architecture and data flow

The permission boundaries path starts with its own permission boundaries evidence admission check, then records topic state, invokes only the needed processor, and finishes at a permission boundaries outcome gate for **permission boundaries**. Keep policy and configuration revisions beside the work, while generated text remains separate from authorization. Measure the bottleneck that belongs to permission boundaries, not a generic agent score.

```mermaid
flowchart LR
  A[Caller] --> I[Identity and tenant]
  I --> C[Context/evidence]
  C --> M[Model proposal]
  M --> B[Policy Decision Point boundary]
  B --> X[Effect or review]
  X --> L[(Evidence log)]
  classDef data fill:#dbeafe,stroke:#2563eb,color:#172554; classDef control fill:#dcfce7,stroke:#15803d,color:#14532d; classDef risk fill:#fee2e2,stroke:#dc2626,color:#450a0a
  class A,C,X,L data; class I,B control; class M risk
```

Keep requested intent, authenticated principal, capability, resource state, policy decision, and effect receipt separate. A model or document can propose a resource but cannot set the caller’s tenant or role. Bind policy revision, resource version, expiry, and decision reason to the authorization record; log references rather than sensitive payloads.

For permission boundaries, record a run identifier, actor, purpose, policy decision point, capability token, resource predicate, row filter, deny default, and confused deputy, policy and model versions, evidence references, decision, attempts, timestamps, and final state. Add the topic's durable artifact—such as a checkpoint, capability, proof status, privacy budget, or provenance chain—rather than assuming a generic transcript can explain the outcome. Keep raw content behind controlled references and retention rules.

## Processing walkthrough and state

Permission state includes requested, scoped, allowed, denied, revoked, expired, and policy_unavailable. Recheck the resource and capability immediately before an effect. A cached decision may support a narrow read for a bounded period, but it must never silently authorize a new write.

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

On retry, reuse the permission boundaries idempotency key or durable artifact; never ask the model to invent a second action when the first attempt has an unknown outcome.

## Topic mechanics: Permission boundaries

### Decision model and topic-specific data contract

Authorization starts with a capability inventory: resource, verb, actor, tenant, purpose, and risk class. The model may propose `create_payment_draft`, but the payment service—not the prompt—checks amount limits, vendor ownership, currency, separation of duties, and approval state. Use deny-by-default policy and return a typed denial that contains a safe reason. Resource predicates matter: a user allowed to read one customer row is not allowed to issue an unrestricted SQL query. Normalize arguments before policy evaluation so alternate encodings cannot bypass a rule. Keep policy decision and effect commit close enough to prevent a time-of-check/time-of-use race; otherwise recheck a version or authorization at commit. Tool descriptions should omit dangerous generic primitives such as unrestricted shell or arbitrary URL fetch. Test indirect prompt injection, confused deputies, cross-tenant IDs, race conditions, and policy outages. A fail-open policy may preserve availability while violating authority; a fail-closed policy may block legitimate work, so define a read-only degraded mode. Frontier's explicit-permission statement is a factual motivation for this boundary; the allow-list, row filter, approval, and race tests are engineering design.

Ask what **permission boundaries** can establish at each transition. The request establishes intent only; the permission boundaries evidence and state stage establishes a bounded representation; the next checker, owner, or reconciliation step establishes whether the proposed result is acceptable. A timeout, missing dependency, or ambiguous response therefore becomes an explicit status for **permission boundaries**, not an implicit success. Persist the relevant versions and evidence references, and retain unknown, deferred, or needs-review states when the system cannot prove the stronger claim.

Permission boundaries require versioned policy rules, resource labels, capability grants, and decision reasons. Include the policy revision in every allow or deny record; revoking a capability must change new decisions while preserving the evidence for actions already authorized.

Permission enforcement should cap resource fan-out, delegation depth, policy-evaluation time, and the lifetime of a capability token. Fail closed when the policy store is unavailable unless a narrowly scoped cached read is explicitly permitted. Expose `policy_unavailable`, `scope_denied`, and `token_expired` as different outcomes.

Break permission boundaries metrics down by task slice, actor or tenant, version, dependency, and outcome class so a healthy average cannot hide a dangerous subgroup.


## Permission boundaries: focused design workshop

In permission boundaries, keep request prose, retrieved evidence, generated proposals, and the lesson artifact in separate typed fields. permission boundaries code owns completeness, freshness, authorization, and promotion of a result; prose only explains intent.

For permission boundaries, the event trail must let an operator distinguish bad input, missing topic evidence, stale state, dependency failure, and a confirmed outcome. Record the permission boundaries artifact and the decision that moved it between states.

Test authorization races. A capability can be revoked after planning but before execution, or a resource can move tenants while a cached decision remains warm. Bind the decision to resource version and expiry, then recheck at the effect owner. Preserve `policy_unavailable` and `revoked` as distinct outcomes; do not convert uncertainty into allow.

For permission boundaries, slice permission boundaries evidence metrics by task class, actor or tenant, governing revision, dependency, and final state. Report the topic invariant, useful completion, latency, cost, and recovery burden together; averages are insufficient when a rare permission boundaries failure carries the largest consequence.

Save a failing permission boundaries input as a regression fixture only after redaction, classification, and capture of the governing version.


## Applications and operational constraints

Start permission boundaries in observation or draft mode, compare against a deterministic or human baseline, then expand only a narrow cohort and reversible effect class.

Beyond **permission boundaries**, permission boundaries applies to workflows where permission boundaries evidence matters. Choose an application with a named owner and bounded effects, then document its data residency, access, quota, staffing, latency, and rollback constraints. The right metric differs by deployment; do not import a support or research target without checking the actual user outcome.

Plan permission capacity around policy evaluation, key rotation, entitlement propagation, and decision logging. If the policy service is overloaded, queue or deny protected effects; do not let a timeout become an implicit allow. Mark cached-read behavior and its expiry so users understand the degraded boundary.

## Failure modes, security, and limits

Permission failures include overbroad roles, confused delegation, stale grants, and fail-open behavior during policy outages. Test resource ownership and revocation at the effect owner, not only in a model gateway. Log the exact capability, policy revision, resource, and reason code so a denial can be investigated without exposing secrets.

Permission metrics can improve by making roles unusably narrow or by excluding denied requests from the denominator. Report legitimate task completion, denied high-risk actions, revocation lag, and policy outages together. A low allow rate is not automatically safe, and a low denial rate is not automatically usable.

For permission boundaries, the February source has a bounded claim. The February source also has scope limits. Frontier says AI coworkers have explicit permissions and guardrails. The February fact is the product's stated boundary model; OWASP and zero-trust principles explain why a model proposal must still be checked by the service that owns the side effect. A prompt is not an authorization mechanism. Nothing in that observation proves robustness against your adversaries, correctness on your domain, or a particular service-level target. Treat vendor examples as source facts and label recommendations as inference. When evidence is weak, abstention and escalation are valid outcomes.

## Evaluation and change management

Build permission fixtures for least-privilege reads, cross-tenant IDs, delegated calls, revocation during execution, policy outage, and duplicate writes. Define the invariant that every effect has a current principal, resource, capability, and policy decision. Keep hostile proposals hidden and test the effect owner independently of the model.

Promote a permission policy only when protected effects, denial explanations, revocation lag, and legitimate completion meet their floors. Shadow decisions where safe, retain an emergency deny or narrow-read mode, and enumerate grants that must be revoked or rechecked after rollback.

## February primary-source evidence

The source fact is bounded: **Frontier says AI coworkers have explicit permissions and guardrails. The February fact is the product's stated boundary model; OWASP and zero-trust principles explain why a model proposal must still be checked by the service that owns the side effect. A prompt is not an authorization mechanism.** The February publication date and the publisher's wording should be cited when teaching the event. The recommendation that teams implement policy decision point, capability token, resource predicate, row filter, deny default, and confused deputy is an inference from the event plus established systems practice. It should be validated with local fixtures, security review, operational metrics, and domain experts. The source does not independently verify the examples, and this article does not present them as guarantees.

## Mini exercise extension

Create six fixtures for **permission boundaries** using the permission boundaries vocabulary: a permission boundaries evidence omission, a stale or contradictory permission boundaries evidence record, an adversarial input, a boundary rejection, a dependency interruption, and a verified completion. Assert different states for each case; do not use one generic success label. Store the evidence reference and recovery owner beside every assertion, then alter the governing version and prove that prior permission boundaries records remain historical.

## Build it locally: numbered implementation

1. Construct a permission boundaries test record with actor, request, permission boundaries evidence, decision, and outcome fields; reject a run that cannot identify the governing version.
2. Implement the permission boundaries boundary as a pure function. It must inspect permission boundaries evidence, return a typed state, and refuse an unrecognized or incomplete transition.
3. Create a deterministic permission boundaries generator with a valid proposal, a malformed proposal, and an input that attempts to redirect the topic-specific decision.
4. Simulate the permission boundaries dependency failing after admission. Use its own correlation or artifact key to detect duplicate delivery and reconcile uncertainty.
5. Write an event stream containing permission boundaries states, redacting sensitive payloads while retaining the evidence pointers needed for an offline replay.
6. Measure permission boundaries correctness alongside rejection rate, time in each state, recovery work, and resource cost; report slices relevant to the lesson.
7. Change the permission boundaries schema or policy revision and verify that old events still resolve under their original contract rather than being reinterpreted.

## Runnable low-cost example

```python
def authorize(subject, tenant, action, amount, approved):
    if tenant != "acme" or action not in {"draft_payment", "read_invoice"}: return False
    return action == "read_invoice" or (amount <= 1000 and approved)
print(authorize("agent", "acme", "draft_payment", 900, True))
print(authorize("agent", "other", "read_invoice", 0, False))
```

This permission sketch demonstrates a deny-by-default branch only. It does not implement authenticated identity, policy distribution, resource ownership, or audit durability; exercise the effect-owning service before using it as a control.

## Interview Q&A

**Q: Where should permission be enforced?** A: Enforce the permission boundaries rule in deterministic code at the resource or artifact boundary; model output may propose, but it cannot authorize or prove the result.

**Q: Why is a model not a permission boundary?** A: Enforce the permission boundaries rule in deterministic code at the resource or artifact boundary; model output may propose, but it cannot authorize or prove the result.

**Q: Which metric would you put on the dashboard first?** A: Track permission boundaries evidence, plus false acceptance or rejection, time spent, resource cost, and recovery; slice results by the permission boundaries risk classes.

**Q: What is the safe response to policy outage?** A: Expose a typed permission boundaries unavailable state, stop unsafe transitions, and reconcile the external dependency before retrying.

**Q: How should permission boundaries be released?** A: Pin permission boundaries evidence and the governing versions, begin with shadow or reversible work, and require the permission boundaries invariant before widening effects.

## Glossary

- **Policy Decision Point**: the topic-specific control boundary that mediates a model proposal and an outcome.
- **Run ID**: the correlation key that joins one permission boundaries attempt to its actor, permission boundaries evidence, decisions, and recovery evidence.
- **Idempotency**: the permission boundaries guarantee that a retry does not create a second logical result or duplicate effect.
- **Provenance**: origin, version, and transformation evidence attached to a permission boundaries input or artifact.
- **SLO**: an explicit permission boundaries service target, such as freshness, verification latency, queue age, or availability.
- **Abstention**: the permission boundaries state used when evidence, authority, or dependency health is insufficient for a stronger claim.
- **Inference**: an engineering recommendation about permission boundaries derived from source facts rather than presented as a source guarantee.

## References

- [OpenAI Frontier — February 5, 2026](https://openai.com/index/introducing-openai-frontier/)
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [NIST SP 800-207](https://www.nist.gov/publications/zero-trust-architecture)

## Claim ledger

| Claim | Source | Fact or inference |
|---|---|---|
| The cited publisher published the February event on the stated date. | [OpenAI Frontier, published February 5, 2026](https://openai.com/index/introducing-openai-frontier/) | Fact |
| Frontier says AI coworkers have explicit permissions and guardrails. | [OpenAI Frontier, published February 5, 2026](https://openai.com/index/introducing-openai-frontier/) | Fact |
| Placing an enforceable authorization boundary between probabilistic proposals and effects. | Engineering design synthesis | Inference |
| A separately enforced boundary is safer and easier to operate than treating model text as authority. | Topic standards and systems reasoning | Inference |
| The local example demonstrates the concept but does not prove production security, reliability, or generalization. | This lesson | Fact about the example |
