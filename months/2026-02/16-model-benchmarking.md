# Model benchmarking
Status: durable
Sources: [HELM](https://crfm.stanford.edu/helm/latest/); [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework); [Google DeepMind's February 11, 2026 Deep Think report](https://deepmind.google/blog/accelerating-mathematical-and-scientific-discovery-with-gemini-deep-think/)
## In one sentence
Meaningful benchmarking tests representative tasks, costs, latency, and failure modes—not one leaderboard score.
## Background: what existed before
Teams selected models from aggregate accuracy numbers disconnected from their workload.
## What changed and why now
System-level evaluation emphasizes scenarios, robustness, and transparent metrics.
## Impact on current processing and architecture
Build a task suite with held-out data, rubric, latency/cost capture, and regression thresholds.
## Real-world applications and constraints
Compare support summarizers or coding agents. Test leakage, sample size, and distribution shift.
## Mental model
```mermaid
flowchart LR
 T[Tasks]-->R[Runner]-->M[Metrics]-->D[Decision]
 R-->C[Cost/latency]
 classDef a fill:#dbeafe,stroke:#2563eb,color:#111827; classDef b fill:#dcfce7,stroke:#16a34a,color:#111827; class T,R a; class M,C,D b
```
```mermaid
sequenceDiagram
 Runner->>Model A: held-out cases
 Runner->>Model B: held-out cases
 Runner-->>Report: quality + cost + failures
 Report-->>Owner: release decision
```
## What changed this month
February frames evaluation as a workload decision rather than a vanity leaderboard.
## Engineering consequence
Report confidence intervals and slice results; keep a fixed regression set.
## Limits and failure modes
Benchmarks can be gamed or stale; human rubrics vary; offline gains may not transfer online.

## SDE2 primer and prerequisites

This lesson is about **model benchmarking** as a production systems problem. A language model is only one stage: an ingress service accepts work, a data layer supplies evidence, an orchestrator keeps state, a policy layer decides what may happen, and an operator or downstream system observes the result. Students should know HTTP, JSON, functions, and basic databases. SDE2 readers should also know queues, authentication, structured logs, metrics, retries, and service-level objectives (SLOs). The central habit is to label what the February source actually reports separately from a recommendation derived from it.

The useful boundary for model benchmarking is **task taxonomy, held-out slice, contamination check, confidence interval, cost-quality frontier, and human rubric**. These are not magic model capabilities. They are interfaces, records, checks, and operating procedures that can be unit-tested. Start with a low-blast-radius workflow and make every external effect attributable to a run ID, actor, policy version, and evidence reference.

## February source reading: fact before inference

The primary February event is **Google DeepMind's February 11, 2026 Deep Think report**. DeepMind reports up to 90% on IMO-ProofBench Advanced, says results were graded by human experts, and reports lower inference-time compute for Aletheia at comparable reasoning quality. The same post shows FutureMath Basic results remain well below its benchmark reference and distinguishes levels of AI contribution. These reported numbers illustrate why a benchmark needs task and protocol context. The report or announcement is evidence about what its publisher described. It is not independent validation of the publisher's claims, and it does not specify your data, threat model, latency budget, or regulatory obligations. That distinction matters because a source can motivate a concept without proving that the concept is solved.

The engineering inference in this lesson is that turning a headline score into a workload decision with slices, cost, latency, and failure analysis. Write that inference as a testable contract: state the accepted inputs, expected transitions, forbidden outcomes, and evidence needed to review a decision. If a test fails, improve the system or narrow the intended use; do not silently reinterpret a source claim as a guarantee.

## Historical baseline and problem boundary

Before this month's event, a team could make a convincing prototype with a synchronous request, a prompt, one model call, and a small script around an API. That baseline remains appropriate for drafting or a read-only experiment. It becomes unsafe or unreliable when a request crosses systems, waits, changes durable data, or must be explained later. The failure is not merely that the model can be wrong. It is that the surrounding software may have no place to record authority, version, evidence, retries, or recourse.

For **comparing two research assistants on verified proof tasks and tool-use cost, not one aggregate score**, draw the boundary before choosing a model. Identify the human or service principal, the records allowed into context, the actions proposed by the model, the component that validates them, and the owner who handles an ambiguous result. Decide which operations are reads, reversible writes, irreversible writes, or merely recommendations. A useful rule is that an untrusted string may influence a proposal but may never create a permission, erase an audit event, or bypass a state transition.

## Architecture and data flow

A deployable design has a control path and a data path. The control path versions configuration, policy, model adapters, schemas, evaluation sets, and rollout cohorts. The data path receives a request, authenticates it, retrieves bounded evidence, invokes the model, validates a typed proposal, executes an allowed action, and records an outcome. The model benchmarking boundary sits between the proposal and the observable outcome; it should be visible in traces and owned by a team.

```mermaid
flowchart LR
  A[Caller] --> I[Identity and tenant]
  I --> C[Context/evidence]
  C --> M[Model proposal]
  M --> B[Task Taxonomy boundary]
  B --> X[Effect or review]
  X --> L[(Evidence log)]
  classDef data fill:#dbeafe,stroke:#2563eb,color:#172554; classDef control fill:#dcfce7,stroke:#15803d,color:#14532d; classDef risk fill:#fee2e2,stroke:#dc2626,color:#450a0a
  class A,C,X,L data; class I,B control; class M risk
```

Use separate fields for user text, retrieved facts, policy instructions, tool output, and generated proposal. This prevents an instruction hidden in a document or tool result from acquiring the authority of a system rule. Every record should carry a tenant or project key where relevant. Cache keys must include authorization scope and source version. Logs should retain enough structured evidence to explain a decision while redacting secrets and unnecessary free text.

A minimal run record is: `run_id`, `request_id`, actor, tenant, purpose, model/version, policy/version, context references, proposal hash, action, decision, timestamps, attempts, effect IDs, and final status. For this topic add task taxonomy, held-out slice, contamination check, confidence interval, cost-quality frontier, and human rubric. Do not put an unbounded transcript in the primary operational table; store a redacted pointer with a retention policy.

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

Persist the proposal before a side effect. On retry, reuse the same idempotency key or proof artifact rather than asking the model to invent a new action. A timeout is a state of knowledge, not proof that nothing happened. For a reversible operation, record the compensating action; for an irreversible operation, stop and escalate. For this lesson, the most important transition is the one that prevents **comparing two research assistants on verified proof tasks and tool-use cost, not one aggregate score** from becoming an unreviewed or untraceable effect.

## Topic mechanics: Model benchmarking

### Decision model and topic-specific data contract

A benchmark is a measurement instrument with a workload model. Start with a taxonomy: routine requests, ambiguous cases, long contexts, tool calls, adversarial inputs, and high-cost or high-risk slices. Freeze a held-out set and record contamination risks, rubric, evaluator version, model configuration, tool permissions, retries, and human intervention. Report a distribution, not just a mean: quality by slice, abstention, critical errors, p50/p95 latency, tokens, dollars, and recovery. A cost-quality frontier often makes a smaller model preferable for routine work and a slower verifier preferable for rare high-impact work. Human grading needs calibration and agreement; automated graders need adversarial tests. DeepMind's February post provides a useful example: it reports up to 90% on IMO-ProofBench Advanced, human grading, lower inference-time compute in Aletheia, and much lower FutureMath Basic performance than its benchmark reference. The contrast warns against moving a score between task families. Test the decision rule itself: would a confidence interval or one costly failure change the procurement choice? Keep a regression set after deployment and audit for leakage.

The first implementation question is what the system can know at each stage. At ingress, it knows an authenticated actor and a request, but not whether the request is well-formed or authorized. During retrieval, it can establish source IDs, freshness, and access filters, but similarity is not truth. During model generation, it can ask for a schema and bounded plan, but the output is still untrusted. At the boundary, deterministic code can enforce limits. After execution, only a receipt, read-after-write check, or independent artifact establishes what happened. This epistemic separation keeps **task taxonomy, held-out slice, contamination check, confidence interval, cost-quality frontier, and human rubric** from collapsing into one prompt.

Benchmarking needs versioned task definitions, scoring code, model checkpoint, decoding settings, hardware, and evaluation split. Publish those alongside the score; changing the denominator or evaluator is a new benchmark result, not a quiet update to the old number.

Benchmark runs should cap cases, decoding attempts, evaluator calls, and hardware time while protecting required slices. A run that cannot execute the full denominator is `incomplete`, not a score. Separate `fixture_error`, `model_failure`, and `evaluator_failure` so a published comparison remains interpretable.

For **model benchmarking**, instrument quality by slice, confidence intervals, p95 latency, token cost, abstention, and critical-error rate. Break down every metric by task slice, tenant, model version, policy version, and outcome class. An aggregate success number can improve while a small high-risk slice becomes worse. Pair capability metrics with reliability metrics and safety metrics; never use one as a proxy for the others.


## Model benchmarking: focused design workshop

The distinctive design choice for this lesson is **task slices and cost-quality decisions**. Model the core record as a typed object with `task_id, slice, score, latency, tokens, evaluator_version`. Keep user prose outside that object; prose can explain intent, but code must decide whether the object is complete, authorized, fresh, and safe to execute. The invariant is: **a headline score cannot hide a critical slice or an unacceptable cost**. Emit an event whenever the invariant is checked, including the result, version, actor, and evidence reference. This makes a failure diagnosable without replaying an unconstrained model call.

Consider a concrete **model benchmarking** run. The ingress validator rejects missing identifiers and normalizes timestamps. The context builder retrieves only records permitted by tenant and purpose. The model receives a bounded view and returns a proposal, never a bearer credential or an opaque instruction. The topic-specific boundary then checks `task_id, slice, score, latency, tokens, evaluator_version`. If the check passes, the effect owner commits or queues work and returns a receipt. If it fails, the system returns a structured denial or asks for evidence. A reviewer can inspect the event sequence and distinguish bad input, missing authority, stale state, and a remote failure.

Test benchmark races. A leaderboard task or evaluator may change while jobs are queued, or a failed protected slice may be hidden by a newly computed aggregate. Freeze split, evaluator, and denominator at admission. Preserve `incomplete` and `evaluator_changed`; neither is a comparable score.

For operations, partition metrics by `task slices and cost-quality decisions` and by model, policy, tenant, and outcome. Track the invariant violation directly, plus useful completion, latency, cost, and human override. A single aggregate can hide a catastrophic slice: one customer, one high-risk action, one rare theorem class, or one overloaded region. Set a release floor for the topic-specific safety metric before optimizing throughput.

The mini design exercise is **choose between two models when one wins average quality but loses a safety slice**. Implement it with an in-memory store first, then add a failure injection at every boundary. Expected behavior should be deterministic even if the proposal generator is not. Save the failing input as a regression fixture only after removing secrets and identifying the policy version that governed it.


## Applications and operational constraints

The strongest first application is **comparing two research assistants on verified proof tasks and tool-use cost, not one aggregate score** because it has a bounded workflow and a domain owner. A team might begin in shadow mode, where the system produces a proposal but performs no effect. Next, allow a canary cohort and only low-risk actions. Require an explicit launch review before expanding scope. The useful outcome is not “the model answered”; it is a completed task that meets quality, latency, cost, privacy, and policy constraints.

Other plausible applications include model selection, coding assistants, scientific tools, and procurement of inference APIs. Each has a different bottleneck. A support system values queue age and consistent escalation; an operations system values correctness and rollback; research values evidence and uncertainty; security values time to detect and false-positive capacity. Data residency, tenant isolation, secrets, rate limits, procurement, and human availability can dominate model latency. Document those constraints in the service contract rather than in an informal prompt.

Plan benchmark capacity around evaluator workers, protected slices, hardware allocation, and artifact retention. If a required slice cannot run, publish an incomplete status rather than a favorable partial score. A cheaper run is valuable only when its denominator and evaluator remain comparable.

## Failure modes, security, and limits

Benchmarking fails through contamination, denominator drift, evaluator leakage, and aggregate scores that hide a protected slice. Keep test data and scoring code controlled, publish confidence or variance where relevant, and require complete run manifests. A leaderboard change is not a model improvement until the task and evaluator remain comparable.

Benchmark metrics can improve through test contamination, hidden prompt tuning, denominator changes, or selecting only favorable tasks. Pair headline scores with protected splits, evaluator audit, confidence intervals, and full run manifests. A leaderboard position is not a general capability claim.

The February source also has scope limits. DeepMind reports up to 90% on IMO-ProofBench Advanced, says results were graded by human experts, and reports lower inference-time compute for Aletheia at comparable reasoning quality. The same post shows FutureMath Basic results remain well below its benchmark reference and distinguishes levels of AI contribution. These reported numbers illustrate why a benchmark needs task and protocol context. Nothing in that observation proves robustness against your adversaries, correctness on your domain, or a particular service-level target. Treat vendor examples as source facts and label recommendations as inference. When evidence is weak, abstention and escalation are valid outcomes.

## Evaluation and change management

Build a fixture set from ordinary, ambiguous, malformed, adversarial, slow, stale, and partially completed cases. Include a golden expected state and the invariants that must never break. Run the set against a pinned model and a deterministic baseline. Review failures by category, not just a total score. Keep hidden cases to detect overfitting, and sample production traces only after removing secrets.

Release gates should include a quality floor, a policy-violation ceiling, a reliability budget, a cost budget, and an evidence-completeness check. Roll out to a small cohort, compare with shadow results, and retain a kill switch that disables risky effects without destroying diagnostic reads. On rollback, record which version was disabled and whether external effects require remediation.

## February primary-source evidence

The source fact is bounded: **DeepMind reports up to 90% on IMO-ProofBench Advanced, says results were graded by human experts, and reports lower inference-time compute for Aletheia at comparable reasoning quality. The same post shows FutureMath Basic results remain well below its benchmark reference and distinguishes levels of AI contribution. These reported numbers illustrate why a benchmark needs task and protocol context.** The February publication date and the publisher's wording should be cited when teaching the event. The recommendation that teams implement task taxonomy, held-out slice, contamination check, confidence interval, cost-quality frontier, and human rubric is an inference from the event plus established systems practice. It should be validated with local fixtures, security review, operational metrics, and domain experts. The source does not independently verify the examples, and this article does not present them as guarantees.

## Mini exercise extension

Create six fixtures for **comparing two research assistants on verified proof tasks and tool-use cost, not one aggregate score**: a normal request, missing evidence, an adversarial instruction, a policy denial, a timeout or interrupted run, and a successful outcome. For each fixture record the expected state, the allowed effect, and the evidence a reviewer should see. Add one version change and prove that the old event retains its original version. Your acceptance criterion is not a polished answer; it is a correct boundary, an explainable decision, and a safe recovery path.

## Build it locally: numbered implementation

1. Define dataclasses for `Request`, `Context`, `Proposal`, `Decision`, `Event`, and `Outcome`; require a run ID and version fields.
2. Write a deterministic boundary function for **task taxonomy, held-out slice, contamination check, confidence interval, cost-quality frontier, and human rubric**; deny unknown actions and malformed arguments.
3. Add a fake model that returns one valid and two invalid proposals, including an instruction hidden in retrieved text.
4. Add a fake downstream service with a timeout, an idempotency map, and a read-after-write reconciliation method.
5. Persist redacted JSON Lines events and implement replay without invoking a live model.
6. Run the six fixtures, assert the security invariant, and calculate quality by slice, confidence intervals, p95 latency, token cost, abstention, and critical-error rate.
7. Change one policy or schema version, rerun the fixtures, and inspect the diff in evidence and state transitions.

## Runnable low-cost example

```python
runs = [{"model":"A","slice":"safety","score":.98,"cost":.10},{"model":"B","slice":"safety","score":.90,"cost":.03}]
chosen = max(runs, key=lambda r: (r["score"], -r["cost"]))
print(chosen)
```

This example is intentionally small and deterministic. It demonstrates the lesson's boundary and its invariant; it does not claim production-grade authentication, durability, isolation, or domain correctness. Extend it with the numbered build steps and failure fixtures before drawing operational conclusions.

## Interview Q&A

**Q: What is the difference between a source fact and an engineering inference?** A: The fact is what a dated publisher says it released, measured, or observed. The inference is a design recommendation derived from that fact and other knowledge; it needs local validation.

**Q: Why separate model output from the boundary?** A: Model output is probabilistic and can be manipulated by input. The boundary is deterministic, attributable code that can enforce authorization, schemas, budgets, and state transitions.

**Q: Which metric would you put on the dashboard first?** A: A useful outcome metric plus a failure metric specific to the topic—quality by slice, confidence intervals, p95 latency, token cost, abstention, and critical-error rate. Pair it with slices so an aggregate cannot hide a critical regression.

**Q: When should the system abstain?** A: When evidence is missing or stale, the policy is ambiguous, the budget is exhausted, or an external effect has an unknown status. Escalate with evidence instead of fabricating confidence.

**Q: What should happen during rollout?** A: Pin versions, start in shadow or canary mode, limit high-risk effects, monitor quality/reliability/safety separately, and keep an audited rollback path.

## Glossary

- **Task Taxonomy**: the topic-specific control boundary that mediates a model proposal and an outcome.
- **Run ID**: a stable identifier joining request, context, decisions, attempts, and effects.
- **Idempotency**: repeating a request produces one logical effect rather than duplicates.
- **Provenance**: evidence describing origin, version, and transformations.
- **SLO**: a measurable service target such as latency or successful completion.
- **Abstention**: an explicit refusal or escalation when evidence or authority is insufficient.
- **Inference**: an engineering conclusion drawn from facts, not a quotation or guarantee from a source.

## References

- [Google DeepMind: Gemini Deep Think — February 11, 2026](https://deepmind.google/blog/accelerating-mathematical-and-scientific-discovery-with-gemini-deep-think/)
- [Stanford HELM](https://crfm.stanford.edu/helm/latest/)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)

## Claim ledger

| Claim | Source | Fact or inference |
|---|---|---|
| The cited publisher published the February event on the stated date. | [Google DeepMind's February 11, 2026 Deep Think report](https://deepmind.google/blog/accelerating-mathematical-and-scientific-discovery-with-gemini-deep-think/) | Fact |
| DeepMind reports up to 90% on IMO-ProofBench Advanced, says results were graded by human experts, and reports lower inference-time compute for Aletheia at comparable reasoning quality. | [Google DeepMind's February 11, 2026 Deep Think report](https://deepmind.google/blog/accelerating-mathematical-and-scientific-discovery-with-gemini-deep-think/) | Fact |
| Turning a headline score into a workload decision with slices, cost, latency, and failure analysis. | Engineering design synthesis | Inference |
| A separately enforced boundary is safer and easier to operate than treating model text as authority. | Topic standards and systems reasoning | Inference |
| The local example demonstrates the concept but does not prove production security, reliability, or generalization. | This lesson | Fact about the example |
