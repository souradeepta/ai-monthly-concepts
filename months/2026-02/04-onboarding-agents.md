# Onboarding agents
Status: emerging
Sources: [OpenAI — 2026-02-05](https://openai.com/index/introducing-openai-frontier/); [Anthropic — tool use](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview)
## In one sentence
Onboarding an agent means explicitly supplying role, tools, constraints, examples, and an observable success contract.
## Background: what existed before
Prompt authors often assumed the model would infer process rules from prose or a few demonstrations.
## What changed and why now
Tool schemas and platform onboarding make capabilities and constraints deployable artifacts, not tribal knowledge.
## Impact on current processing and architecture
Initialization becomes a tested configuration phase before the task loop.
## Real-world applications and constraints
Useful when teams hand off agents across environments. Context size, stale examples, and conflicting instructions are risks.
## Mental model
```mermaid
flowchart LR
 R[Role]-->K[Constraints]-->T[Typed tools]-->E[Examples]-->L[Loop]
 classDef c fill:#dbeafe,stroke:#2563eb,color:#111827; classDef g fill:#dcfce7,stroke:#16a34a,color:#111827; class R,E c; class K,T,L g
```
```mermaid
sequenceDiagram
 Config->>Agent: role + policy + schemas
 Agent->>Validator: self-check
 Validator-->>Agent: ready or missing field
 Agent->>Tool: validated call
```
## What changed this month
The February framing treats onboarding as lifecycle engineering around the model.
## Engineering consequence
Version onboarding bundles and test them with adversarial and ordinary tasks.
## Limits and failure modes
Examples can overfit; instructions can conflict; schemas constrain syntax but not truthfulness.

## SDE2 primer and prerequisites

This lesson treats **onboarding agents** as a controlled activation problem. An applicant declares a capability, reviewers inspect risk, a sandbox exercises tools, and an owner accepts responsibility for the live scope. Students should know HTTP, JSON, authentication, and basic databases. For SDE2 work, add queues, structured logs, metrics, rollback, and service-level objectives (SLOs). Separate the source’s product claims from readiness evidence that a local team must collect.

The useful boundary for onboarding agents is **role contract, tool manifest, readiness probe, examples, escalation rule, and configuration version**. These are not magic model capabilities. They are interfaces, records, checks, and operating procedures that can be unit-tested. Start with a low-blast-radius workflow and make every external effect attributable to a run ID, actor, policy version, and evidence reference.

## February source reading: fact before inference

For onboarding agents, read the February source through its own claim boundary. The cited February event is **OpenAI Frontier, published February 5, 2026**. Frontier's authors compare agent deployment with employee onboarding: understanding how work is done, having tools, learning what good looks like, and receiving identity and boundaries. The post also says the platform can use existing data and applications through open standards. It does not prove that any particular prompt or schema will work for a new organization. The report or announcement is evidence about what its publisher described. It is not independent validation of the publisher's claims, and it does not specify your data, threat model, latency budget, or regulatory obligations. That distinction matters because a source can motivate a concept without proving that the concept is solved.

For onboarding agents, the engineering inference is narrower: turn the cited capability into an operational contract with topic-specific inputs, states, evidence, and failure ownership. Test that contract against ordinary, adversarial, stale, and interrupted work. A source can motivate this design; it cannot guarantee the resulting reliability or safety.

## Historical baseline and problem boundary

The useful onboarding baseline is a prompt and a team-owned API key deployed for a pilot. That is fast for exploration, but it hides who owns the agent, which data it can see, and how it will be disabled. Onboarding turns that informal experiment into a reviewed capability with explicit scope and accountability.

The onboarding boundary separates the requested role, verified configuration, readiness evidence, and activation decision. Treat read evidence, model proposals, and committed effects as different data classes. A request can influence a proposal but cannot grant authority. Test this boundary with stale, malformed, replayed, and partially completed cases.

## Architecture and data flow

The onboarding path starts with owner and scope admission, records manifest and policy versions, runs readiness probes, and finishes at activation, rejection, or pending review. Keep policy and configuration revisions beside the work, while generated text remains separate from authorization. Measure tool-test coverage, review age, and post-activation correction—not a generic agent score.

```mermaid
flowchart LR
  A[Caller] --> I[Identity and tenant]
  I --> C[Context/evidence]
  C --> M[Model proposal]
  M --> B[Role Contract boundary]
  B --> X[Effect or review]
  X --> L[(Evidence log)]
  classDef data fill:#dbeafe,stroke:#2563eb,color:#172554; classDef control fill:#dcfce7,stroke:#15803d,color:#14532d; classDef risk fill:#fee2e2,stroke:#dc2626,color:#450a0a
  class A,C,X,L data; class I,B control; class M risk
```

Keep the application request, agent manifest, review evidence, sandbox result, and activation decision separate. This lets an operator see whether a capability was requested, tested, approved, or actually enabled. Bind owner, tenant, data class, tool set, manifest revision, and expiry to the activation record while minimizing transcript retention.

For onboarding agents, record a run identifier, actor, purpose, role contract, tool manifest, readiness probe, examples, escalation rule, and configuration version, policy and model versions, evidence references, decision, attempts, timestamps, and final state. Add the topic's durable artifact—such as a checkpoint, capability, proof status, privacy budget, or provenance chain—rather than assuming a generic transcript can explain the outcome. Keep raw content behind controlled references and retention rules.

## Processing walkthrough and state

Onboarding state should distinguish submitted, evidence_pending, security_review, sandbox_failed, approved, activated, suspended, and withdrawn. Recheck owner and manifest at activation, and make withdrawal idempotent. A completed form is not proof that tools are safe or that the agent is still owned.

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

On retry, reuse the onboarding agents idempotency key or durable artifact; never ask the model to invent a second action when the first attempt has an unknown outcome.

## Topic mechanics: Onboarding agents

### Decision model and topic-specific data contract

An onboarding bundle should be compiled like an API client. Start with a role contract that states the task, non-goals, escalation conditions, and evidence standard. Add a tool manifest with JSON schemas, examples, read/write labels, quotas, and error meanings. Separate policy instructions from domain reference material, because reference text may be stale or adversarial. A readiness probe can ask the agent to summarize its allowed actions, refuse a forbidden action, and produce a valid tool call for a fixture. For the support handoff case, include examples of billing ambiguity, angry customers, missing account data, and an outage; the desired behavior is often to ask a question or escalate rather than improvise. Version the bundle and test it in CI against a held-out fixture set. Configuration drift is a production bug: a tool added to development but absent in production should fail readiness, while a production-only tool should not silently appear in the prompt. Track first-run success and invalid-call rate by bundle version. OpenAI's open-standards framing supports portability as a product goal, but portability does not mean every model interprets descriptions identically; adapter tests remain necessary.

Onboarding establishes that a proposed configuration has been reviewed and tested; it does not establish that every future task will be safe. A timeout, missing dependency, or ambiguous test therefore becomes an explicit pending or failed state, not an implicit approval. Persist manifest, policy, model, and evaluator versions with the activation decision.

Onboarding needs a versioned agent manifest, tool inventory, training checklist, owner assignment, and approval record. A manifest change should create a new reviewable revision; an audit trail must still show which capabilities were enabled when an earlier run occurred.

Onboarding needs gates on the number of pending reviews, requested tools, data classes, and unresolved training tasks. Do not provision an agent whose owner or rollback plan cannot be verified. Return `review_queue_full`, `owner_missing`, or `capability_not_ready` distinctly so applicants know what must change.

Break onboarding metrics down by task, tenant, tool, manifest version, reviewer, dependency, and outcome so a healthy approval average cannot hide an unsafe capability.


## Onboarding agents: focused design workshop

Keep the application request, agent manifest, review evidence, sandbox results, and activation decision in separate typed fields. Provisioning code owns completeness and scope; prose only explains the intended role.

The event trail should distinguish missing owner, unclassified data, failed tool test, expired review, policy denial, and activation. Record the manifest digest and decision actor, never just a final “ready” label.

Test onboarding races. An agent can pass review while its owner leaves, a tool contract changes, or a data classification is tightened before activation. Recheck manifest revision and owner status at provisioning time. Preserve `activation_pending` and `review_expired` as explicit states; never treat a submitted checklist as evidence that a capability is ready.

Slice readiness metrics by task, tenant, data class, tool, governing revision, dependency, and final state. Report post-activation correction, rollback, and owner response alongside approval time.

Save failed readiness cases as redacted fixtures with manifest digest, policy version, tool scope, expected state, and recovery owner.


## Applications and operational constraints

Start with observation or draft-only behavior, compare sandbox results with a deterministic or human baseline, then activate a narrow tool set for a small cohort. Expand only after the owner, rollback, and adverse-case evidence is complete.

Onboarding matters for support, finance, deployment, and research agents that will be handed from one team to another. Each application needs a named owner, data-residency decision, access scope, quota, staffing plan, latency budget, and rollback or kill switch. A shared onboarding template should standardize evidence without pretending every domain has the same risk.

Plan onboarding capacity around reviewers, security assessments, sandbox slots, and support ownership rather than model throughput alone. A full review queue should stop new activation, not hide the backlog with automatic approvals. Show applicants whether the agent is pending, rejected, or activated with a bounded capability set.

## Failure modes, security, and limits

Onboarding fails when a checklist is mistaken for readiness. Watch for unowned agents, excessive initial scope, untested tools, missing data classification, and reviewers approving copied risk assessments. Require a capability inventory, sandbox trial, rollback owner, and post-activation check; activation evidence should remain available for later withdrawal.

Onboarding metrics can be gamed by closing applications quickly, narrowing declared scope, or approving agents before their tools are tested. Pair activation time with post-launch incidents, rollback use, owner response, and capability coverage. A high approval rate is not evidence of readiness when reviewers rarely inspect adverse cases.

The source claim is bounded: Frontier compares agent deployment with employee onboarding, including understanding work, using tools, learning what good looks like, and receiving identity and boundaries. It also describes integration with existing applications through open standards. Those are publisher claims; a local readiness bundle, sandbox, and approval gate are engineering inferences that require testing.

## Evaluation and change management

Build onboarding fixtures for missing owners, excessive tools, sensitive data, failed sandbox tests, reviewer disagreement, expired approvals, and rollback. Define the activation invariant and expected capability scope. Run them through the same provisioning gate used in production, with hidden adverse cases and redacted application traces.

Activate an agent only when owner, data classes, tool tests, escalation, and rollback evidence are complete. Start with a small capability cohort, retain a disable switch that preserves audit reads, and record which tools and users were affected if activation is withdrawn.

## February primary-source evidence

The source fact is bounded: **Frontier's authors compare agent deployment with employee onboarding: understanding how work is done, having tools, learning what good looks like, and receiving identity and boundaries. The post also says the platform can use existing data and applications through open standards. It does not prove that any particular prompt or schema will work for a new organization.** The February publication date and the publisher's wording should be cited when teaching the event. The recommendation that teams implement role contract, tool manifest, readiness probe, examples, escalation rule, and configuration version is an inference from the event plus established systems practice. It should be validated with local fixtures, security review, operational metrics, and domain experts. The source does not independently verify the examples, and this article does not present them as guarantees.

## Mini exercise extension

Create six fixtures: missing owner, excessive tool scope, sensitive data without classification, failed sandbox test, expired approval, and successful read-only activation. Assert distinct states and preserve the governing manifest and policy versions.

## Build it locally: numbered implementation

1. Define a manifest with owner, role, tenant, data classes, tools, model adapter, policy revision, SLO, and kill switch.
2. Validate that every tool has a schema, side-effect label, quota, error contract, and sandbox fixture.
3. Run ordinary, malformed, adversarial, and forbidden-task probes against the proposed bundle.
4. Require security and domain review for sensitive data, writes, or external communication.
5. Store an activation decision with manifest digest, reviewer, expiry, and permitted cohort.
6. Monitor invalid calls, escalation, correction, rollback, and owner response after activation.
7. Withdraw the bundle idempotently when ownership, policy, or tool scope changes.

## Runnable low-cost example

```python
bundle = {"role":"support triage", "tools":{"search":{"required":["query"]}}, "excludes":{"delete"}, "version":"b4"}
def ready(b):
    return "search" in b["tools"] and "delete" in b["excludes"] and b["version"]
print(ready(bundle))
```

This provisioning sketch checks a manifest invariant in memory. It does not perform security review, sandboxing, owner verification, or rollback; extend it with denied and incomplete applications before treating activation as safe.

## Interview Q&A

**Q: What proves an agent is ready?** A: A complete manifest, named owner, tested tools, adverse-case evidence, approval, rollback path, and a defined activation scope.

**Q: Why separate activation from application?** A: Review is a release decision; application runs are later evidence that the activated scope is working as intended.

**Q: Which metric would you put on the dashboard first?** A: Post-activation invalid-call and rollback rates, split by tool and manifest version, alongside legitimate completion.

**Q: When should onboarding stop?** A: Stop activation when ownership, classification, tool tests, evidence, or rollback is missing, or when protected slices regress.

**Q: How should onboarding agents be released?** A: Version the bundle, shadow it, canary a small read-only scope, and widen only after readiness and post-launch guardrails pass.

## Glossary

- **Role contract**: the task, non-goals, escalation rules, and evidence standard for an agent.
- **Tool manifest**: the versioned inventory of tools, schemas, side effects, quotas, and errors.
- **Readiness probe**: a test that checks whether the proposed bundle behaves correctly on safe fixtures.
- **Activation**: the controlled transition from reviewed configuration to an allowed runtime scope.
- **Idempotency**: behavior in which repeating one provisioning command does not duplicate activation.
- **Provenance**: origin, version, and transformation evidence attached to setup or test results.
- **Abstention**: a decision to remain inactive when evidence, authority, or dependency health is insufficient.

## References

- [OpenAI Frontier — February 5, 2026](https://openai.com/index/introducing-openai-frontier/)
- [Anthropic tool use overview](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview)

## Claim ledger

| Claim | Source | Fact or inference |
|---|---|---|
| The cited publisher published the February event on the stated date. | [OpenAI Frontier, published February 5, 2026](https://openai.com/index/introducing-openai-frontier/) | Fact |
| Frontier's authors compare agent deployment with employee onboarding: understanding how work is done, having tools, learning what good looks like, and receiving identity and boundaries. | [OpenAI Frontier, published February 5, 2026](https://openai.com/index/introducing-openai-frontier/) | Fact |
| Treating setup as a versioned release artifact with tests, owners, and a readiness gate. | Engineering design synthesis | Inference |
| A separately enforced boundary is safer and easier to operate than treating model text as authority. | Topic standards and systems reasoning | Inference |
| The local example demonstrates the concept but does not prove production security, reliability, or generalization. | This lesson | Fact about the example |
