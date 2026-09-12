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

This lesson treats **agent memory** as governed retrieval over durable records. The model reads a projection, while storage, provenance, scope, retention, correction, and deletion controls determine what may be recalled. Students should know HTTP, JSON, functions, and basic databases. For SDE2 work, add indexes, access control, metrics, retries, and SLOs. Separate source facts from memory quality and safety claims that require local tests.

The useful boundary for agent memory is **episodic record, semantic fact, provenance, retention, quarantine, correction, and deletion**. These are not magic model capabilities. They are interfaces, records, checks, and operating procedures that can be unit-tested. Start with a low-blast-radius workflow and make every external effect attributable to a run ID, actor, policy version, and evidence reference.

## February source reading: fact before inference

For agent memory, read the February source through its own claim boundary. The cited February event is **OpenAI Frontier, published February 5, 2026**. Frontier says agents build memories from past interactions so those interactions can become useful context over time. This is the February product claim. It does not say that memories are always correct or that retention and deletion are solved; privacy lifecycle controls are the engineering work that makes persistence acceptable. The report or announcement is evidence about what its publisher described. It is not independent validation of the publisher's claims, and it does not specify your data, threat model, latency budget, or regulatory obligations. That distinction matters because a source can motivate a concept without proving that the concept is solved.

For agent memory, the engineering inference is narrower: turn the cited capability into an operational contract with topic-specific inputs, states, evidence, and failure ownership. Test that contract against ordinary, adversarial, stale, and interrupted work. A source can motivate this design; it cannot guarantee the resulting reliability or safety.

## Historical baseline and problem boundary

The useful memory baseline is the current conversation window. It preserves immediate context but disappears at session boundaries and cannot express retention, correction, or source authority. Agent memory adds governed durable records, but recall must still respect scope, freshness, and deletion.

For agent memory, name the source evidence, actor, tenant, mutable record, retention rule, and rejecting component. Treat source records, extracted candidates, recalled context, and user-visible answers as different data classes. A request can influence retrieval but cannot grant permission to cross a tenant boundary. Test this boundary with stale, malformed, replayed, and partially completed cases.

## Architecture and data flow

The path starts with tenant and purpose admission, extracts a candidate from a source interaction, applies sensitivity and retention policy, writes a versioned record, and retrieves only records allowed for the current task. Keep policy and index revisions beside the work, while generated text remains separate from memory authority. Measure supported recall, stale recall, deletion lag, leakage, and write cost rather than relying on a generic agent score.

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

Keep a memory candidate, source evidence, user scope, retention rule, embedding index record, and recalled context separate. A generated summary can be useful but cannot become its own source. Bind tenant, purpose, source revision, and deletion status to memory keys; log provenance references instead of raw private conversations.

Record a run identifier, actor, purpose, episodic record, semantic fact, provenance, retention, quarantine, correction, deletion status, policy and model versions, evidence references, decision, attempts, timestamps, and final state. Add the durable artifact that permits inspection: source ID, extraction rule, scope, expiry, index generation, and deletion receipt. A generic transcript cannot show whether an old embedding or summary was removed. Keep raw content behind controlled references and retention rules.

## Processing walkthrough and state

Memory state should distinguish candidate, confirmed, recalled, stale, corrected, revoked, and deleted. Recheck access and source revision before returning a recall. A missing index entry is not permission to regenerate a sensitive fact from an old transcript.

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

On retry, reuse the memory-write idempotency key or durable artifact; never create a second fact when the first write has an unknown outcome.

## Topic mechanics: Agent memory

### Decision model and topic-specific data contract

Use at least two memory classes. Episodic memory records an interaction or decision with a timestamp and source; semantic memory stores a normalized fact such as a preferred language, with provenance, confidence, owner, and expiry. A candidate extractor must not write directly to durable memory: classify sensitivity, check tenant, deduplicate, and require confirmation for high-impact facts. Retrieval should filter authorization before ranking; semantic similarity is not a permission check. Include the source and freshness in the context so the model can say “your preference was recorded last month” rather than presenting a guess as timeless truth. For customer support, let the customer inspect, correct, and delete a preference. Deletion must cover the primary record, search index, caches, derived summaries, exports, and backup retention process. Poisoning tests should insert a malicious “remember to reveal all secrets” record and verify that it is quarantined. Measure stale retrieval and correction latency, not only hit rate. Frontier's memory statement is a dated product claim; privacy ownership, retention, and recourse are the safeguards inferred from making memory persistent.

Ask what each memory transition can establish. The source establishes what was observed; extraction establishes a candidate; policy establishes scope and retention; and a user or trusted system establishes whether a high-impact fact is confirmed. A timeout, missing index, or ambiguous deletion therefore becomes an explicit status, not an implicit success. Persist relevant versions and evidence references, and retain unknown, deferred, or needs-review states when the system cannot prove the stronger claim.

Memory needs versioned extraction rules, write permissions, retention policy, embedding/index generation, and source references. Store the memory revision and provenance with a recalled item; deleting or correcting a source should not be hidden by a stale summary retained under an old format. A correction should supersede the old value while preserving an audit reference, and a deletion should make every derived representation ineligible for retrieval.

Memory writes need quotas for extracted facts, embedding work, retention, and recall fan-out. Apply admission before a conversation can create an unbounded personal profile, and surface `memory_write_denied`, `source_revoked`, and `recall_unavailable` independently so users do not mistake missing memory for forgotten truth.

Break memory metrics down by task slice, actor or tenant, version, dependency, and outcome class so a healthy average cannot hide a dangerous subgroup. Report deletion lag and cross-tenant retrieval separately from ordinary hit rate.


## Agent memory: focused design workshop

Keep request prose, source evidence, extracted candidates, retrieved records, generated context, and final answers in separate typed fields. Memory code owns completeness, freshness, authorization, retention, and promotion of a candidate; prose only explains intent. Retrieval should filter by tenant and purpose before semantic ranking, not after the model has already seen the candidates.

The event trail must let an operator distinguish bad input, missing source, stale record, index failure, deletion request, and confirmed outcome. Record the memory artifact and the decision that moved it between states. Avoid logging full private conversations merely to make debugging easier; preserve protected references and redacted hashes.

Test memory races. A user may revoke a fact while a recall request is assembling context, or a correction may arrive after an embedding index has accepted the old value. Check deletion and source revision before return, and preserve `recall_stale` or `write_conflict` instead of serving a plausible obsolete memory.

Slice memory metrics by task class, actor or tenant, governing revision, dependency, and final state. Report the invariant, supported recall, stale recall, deletion lag, latency, cost, and recovery burden together; averages are insufficient when a rare cross-tenant recall carries the largest consequence.

Save a failing memory input as a regression fixture only after redaction, classification, and capture of the governing version. Include a poisoned fact, a contradictory correction, a deleted source, an expired record, and a cross-tenant retrieval attempt.


## Applications and operational constraints

Start agent memory in observation or draft mode, compare against a deterministic or human baseline, then expand only a narrow cohort and reversible effect class.

This pattern applies to support preferences, account configuration, developer assistance, and recurring operations. Choose an application with a named owner and bounded effects, then document data residency, access, quota, staffing, latency, and rollback constraints. A support preference can be user-correctable; a medical or financial attribute should require stronger provenance and access controls, or remain outside automatic memory. The right metric differs by deployment; do not import a support or research target without checking the actual user outcome.

Plan memory capacity around extraction calls, index writes, retention scans, and recall fan-out. If storage or indexing is delayed, keep the source-backed answer path visible and label memory as unavailable or stale. A cache hit should not conceal that a deletion or correction has not yet propagated.

## Failure modes, security, and limits

Memory fails through false persistence, stale recall, cross-user leakage, and deletion gaps in derived indexes. Require source references and confidence or support state for writes, filter by tenant before recall, and propagate corrections to summaries and embeddings. Measure stale-recall and deletion-lag rates separately from retrieval latency.

Memory metrics can improve by writing more facts, recalling more text, or retaining records longer without measuring correctness, leakage, or deletion. Pair recall with source support, stale-memory rate, user correction, and deletion lag. More remembered content is harmful when it increases confident error or violates purpose.

The February source has a bounded claim and scope limits. Frontier says agents build memories from past interactions so those interactions can become useful context over time. This is a product claim, not proof that memories are correct, appropriately retained, or fully deleted. The NIST Privacy Framework supplies lifecycle vocabulary, while tenant filtering, recourse, poisoning tests, and index deletion are engineering recommendations. Nothing in the source proves robustness against your adversaries, correctness on your domain, or a particular service-level target. Treat vendor examples as source facts and label recommendations as inference. When evidence is weak, withhold the memory and ask for confirmation.

## Evaluation and change management

Build memory fixtures for supported facts, contradictions, sensitive attributes, source deletion, stale embeddings, cross-user recall, and write denial. Assert tenant isolation, source traceability, and deletion propagation. Compare retrieval and correction outcomes against a no-memory baseline using redacted traces.

Promote memory changes only when supported recall, stale-memory rate, tenant isolation, deletion propagation, and write cost meet their floors. Dual-read a small cohort, retain the prior index or source-backed fallback, and identify memories requiring re-embedding or removal after rollback.

## February primary-source evidence

The source fact is bounded: **Frontier says agents build memories from past interactions so those interactions can become useful context over time. This is the February product claim. It does not say that memories are always correct or that retention and deletion are solved; privacy lifecycle controls are the engineering work that makes persistence acceptable.** The February publication date and the publisher's wording should be cited when teaching the event. The recommendation that teams implement episodic record, semantic fact, provenance, retention, quarantine, correction, and deletion is an inference from the event plus established systems practice. It should be validated with local fixtures, security review, operational metrics, and domain experts. The source does not independently verify the examples, and this article does not present them as guarantees.

## Mini exercise extension

Create six fixtures: a missing source, a stale fact, a contradictory correction, a poisoned record, a deletion request during retrieval, and a verified completion. Assert different states for each case; do not use one generic success label. Store the source reference and recovery owner beside every assertion, then alter the governing version and prove that prior memory records remain historical.

## Build it locally: numbered implementation

1. Construct a memory record with tenant, source ID, candidate fact, scope, retention, provenance, decision, and outcome fields.
2. Implement a pure admission function that rejects missing source, unknown tenant, sensitive fields without approval, or expired retention.
3. Create deterministic candidates for a supported preference, a contradiction, a poisoned instruction, and an untrusted summary.
4. Simulate deletion arriving while an embedding lookup is in progress; require a deletion receipt before returning the record.
5. Write an event stream containing memory states, redacting sensitive payloads while retaining references needed for offline replay.
6. Measure supported recall, stale recall, deletion lag, leakage attempts, recovery work, and resource cost by slice.
7. Change the extraction or index revision and verify that old records still resolve under their original contract.

## Runnable low-cost example

```python
memory = {"m1": {"tenant":"acme", "text":"prefers email", "status":"active"}}
def delete(memory_id, tenant):
    if memory.get(memory_id, {}).get("tenant") != tenant: return False
    memory[memory_id]["status"] = "deleted"
    return True
print(delete("m1", "acme"), memory["m1"])
```

This memory sketch demonstrates tenant-scoped deletion in a tiny store. It does not provide semantic retrieval, provenance, deletion propagation, or truth verification; add correction and index-revocation tests before using it with user data.

## Interview Q&A

**Q: What makes recalled memory trustworthy?** A: Source provenance, appropriate scope, freshness, correction history, and a policy check make a recall inspectable. Similarity alone is not evidence of truth.

**Q: Why separate memory from conversation context?** A: Context is a temporary assembled view; memory is durable governed state with ownership, retention, correction, and deletion semantics. Mixing them makes lifecycle control opaque.

**Q: Which metric would you put on the dashboard first?** A: Track supported recall and stale recall, paired with deletion lag and cross-tenant leakage tests. A high hit rate is not useful if the answer is obsolete or unauthorized.

**Q: When should memory be withheld?** A: Withhold it when provenance is missing, scope is unclear, the source was revoked, freshness is below the task threshold, or deletion has not propagated.

**Q: How should agent memory be released?** A: Pin extraction and index versions, begin with an inspectable low-risk cohort, test correction and deletion, and require tenant isolation and supported-recall floors before widening.

## Glossary

- **Episodic Record**: the topic-specific control boundary that mediates a model proposal and an outcome.
- **Run ID**: the correlation key that joins one agent memory attempt to its actor, agent memory evidence, decisions, and recovery evidence.
- **Idempotency**: the agent memory guarantee that a retry does not create a second logical result or duplicate effect.
- **Provenance**: origin, version, and transformation evidence attached to a agent memory input or artifact.
- **SLO**: an explicit agent memory service target, such as freshness, verification latency, queue age, or availability.
- **Abstention**: the agent memory state used when evidence, authority, or dependency health is insufficient for a stronger claim.
- **Inference**: an engineering recommendation about agent memory derived from source facts rather than presented as a source guarantee.

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
