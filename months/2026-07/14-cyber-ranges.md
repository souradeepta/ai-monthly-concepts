# Cyber ranges
Status: emerging
Sources: [NIST — Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework) (primary guidance); [MITRE ATT&CK](https://attack.mitre.org/) (public knowledge base)

## In one sentence
A cyber range is an isolated, instrumented environment where teams can measure an AI system’s security behavior against realistic scenarios without exposing production systems or publishing harmful operational recipes.

## Background: what existed before

Security testing began with code review, vulnerability scanning, and tabletop exercises. These remain useful, but each sees only part of a system. A scanner can identify a vulnerable package without showing whether an agent will misuse a tool. A tabletop can reveal an unclear escalation path without producing telemetry. A production exercise can produce realism at the cost of customer impact. A cyber range occupies the middle: it supplies controlled infrastructure, synthetic identities, repeatable scenarios, and a clear reset operation.

An AI security range has an extra boundary. The system under test may generate text, call tools, interpret logs, or plan multi-step work. A test scenario therefore needs to represent both an environment and an authority budget. The range should make it possible to ask “did the agent detect and report the unsafe condition?” without handing learners a copy-paste attack path against a real service.

## What changed and why now

The change is from static challenge machines to measured agent environments. A contemporary range can expose a help-desk queue, a fake cloud account, or a small network graph through safe APIs. It records actions, policy decisions, and recovery behavior. The scenario is versioned like a test fixture, and reset is part of the test contract. NIST’s framework and MITRE’s knowledge base provide source context for organizing outcomes and tactics; applying them to an agent-specific range is an engineering inference.

The range must separate three audiences: the learner, the evaluator, and the operator. Learners receive only the task and permitted interfaces. Evaluators receive assertions and telemetry. Operators receive reset, quarantine, and emergency-stop controls. If all users receive unrestricted shell access to the same environment, the range becomes a distribution mechanism for dangerous procedures instead of a measurement system.

## Impact on current processing and architecture

Begin with a scenario manifest. It identifies the seed, services, synthetic assets, user roles, allowed actions, time limit, success criteria, and cleanup policy. An orchestrator provisions the scenario from an immutable image. A gateway exposes only declared tools. An event collector receives structured records from the agent and environment. A scorer evaluates behavior against assertions rather than rewarding a particular string.

```mermaid
flowchart TB
  S[Scenario manifest] --> O[Range orchestrator]
  O --> I[Immutable environment]
  I --> T[Instrumented services]
  A[Agent under test] --> G[Tool and network gateway]
  G --> I
  I --> E[Event collector]
  A --> E
  E --> V[Assertions and scorer]
  V --> R[Report and reset]
  classDef input fill:#dbeafe,stroke:#2563eb,color:#111827
  classDef boundary fill:#dcfce7,stroke:#16a34a,color:#111827
  classDef risk fill:#fee2e2,stroke:#dc2626,color:#111827
  class S,A input
  class O,G,E boundary
  class I,T risk
```

Telemetry needs a schema. Useful fields include scenario ID, run ID, timestamp, principal, tool name, target class, decision, result class, and correlation ID. Do not log live secrets, even synthetic ones, in plain text. Hash or label them. Keep the agent’s raw transcript separate from security events because transcripts can contain sensitive task data and are often much larger.

## Real-world applications and constraints

A platform team can test whether a coding agent refuses to expose a fake credential in a repository. A security team can evaluate whether a triage agent distinguishes an alert from an instruction embedded in an alert payload. A robotics team can simulate a compromised device and check that the fleet controller isolates it. A training organization can provide graded scenarios without allowing participants to contact external hosts.

Realism is expensive and can be misleading. A small range may omit identity propagation, queue delays, or noisy telemetry found in production. A detailed range may consume substantial compute and create fragile tests. Synthetic data must still have realistic formats and relationships; otherwise the model learns to recognize a toy marker. Scenarios need an expiration date because dependencies, model versions, and defensive controls change.

## Mental model

Treat a range as a laboratory, not a playground. The scenario is an experiment, the agent is the subject, the assertions are hypotheses, and telemetry is evidence. A good result is reproducible: another run with the same seed should have comparable initial conditions. A good failure is diagnosable: the report should show which authority was available, what the agent observed, which action it proposed, and why the assertion failed.

The range has two safety invariants. First, no route should lead from the range to an uncontrolled production or public target. Second, reset must remove state created by the run, including scheduled jobs, credentials, files, and queued messages. A hidden “cleanup” script that misses one resource is not a reset guarantee.

## What changed this month

The July learning map adds cyber ranges alongside cybersecurity evaluation and red teaming. The month-specific connection is an engineering inference: agent systems require repeatable environments that test tool use and recovery, not only response text. This article makes no claim that a particular July release introduced a cyber range.

## Engineering consequence

Write scenario contracts before building dashboards. For each test, state what counts as capability, what counts as unsafe behavior, and what evidence distinguishes the two. A refusal can be a failure if the task was authorized and harmless; a successful action can be a failure if it crossed a prohibited boundary. Score at least action safety, detection quality, containment time, and operator escalation separately.

```mermaid
sequenceDiagram
  participant Q as Test runner
  participant O as Orchestrator
  participant X as Range
  participant A as Agent
  participant Sc as Scorer
  Q->>O: create scenario with seed
  O->>X: provision isolated resources
  X-->>Q: run ID and tool endpoint
  Q->>A: provide bounded task
  A->>X: observe and request action
  X-->>A: result and telemetry
  alt assertion event
    X->>Sc: emit correlated evidence
  else timeout or boundary violation
    O->>X: quarantine and stop
    X->>Sc: emit failure evidence
  end
  Sc-->>Q: score, traces, reset status
  Q->>O: destroy run
```

Use layers of isolation: a separate cloud account or project, deny-by-default network rules, per-run service accounts, resource quotas, and an outer kill switch. The gateway should reject undeclared destinations before DNS resolution where possible. Tool calls should be typed and validated. If a scenario intentionally includes an insecure service, keep it behind a private range address and seed it with non-sensitive data.

The test runner should support deterministic replay where feasible. Freeze the seed, fixture versions, and initial queue contents. External model calls may be nondeterministic, so record model version, sampling settings, and tool observations. Replay is not proof of identical reasoning; it is a way to compare externally visible behavior and locate regressions.

## Limits and failure modes

A benchmark can be gamed. If success depends on one keyword, an agent can emit it without understanding the scenario. If the environment is too predictable, the test measures memorization. If assertions ignore time, a late containment may look as good as an immediate one. If logs are incomplete, a safe action can look suspicious or a harmful side effect can disappear from the report.

Scenario design should vary the surface while preserving the underlying question. For a data-exposure test, change field names, queue order, and message wording across seeds, then retain the invariant that a confidential field cannot be sent to an untrusted destination. For an authorization test, vary whether permission is explicit, expired, or delegated. This prevents a model from passing by spotting a fixed marker. At the same time, each variation needs a human-readable rationale so that a failing test can be reviewed rather than treated as an opaque score.

Instrumentation should be designed before the exercise. Capture the policy decision before a tool call, the normalized tool arguments, the service response class, and the resulting state transition. A trace that contains only model messages cannot show whether a gateway blocked a request or whether the model never attempted it. Conversely, raw payload capture may expose more data than the exercise requires. Prefer typed summaries, stable IDs, and hashes for large objects; retain the original only under an explicit incident flag.

Containment is an operational workflow. A quota breach should stop new work, revoke the run identity, preserve a minimal trace, and alert the range operator. A malformed scenario should be marked invalid rather than counted as an agent failure. If a service becomes unavailable, the runner should distinguish infrastructure failure from agent behavior. These categories matter when teams decide whether to change a prompt, a policy, the environment, or the test itself.

Ranges also support progressive difficulty. Start with one tool and a clear policy, then introduce delayed responses, conflicting records, expired authorization, or a human approval queue. Increase one source of complexity at a time. Otherwise a failure gives no useful diagnosis. Record the difficulty level in the report and compare agents only on scenarios with equivalent authority and observability.

A useful report explains the counterfactual. If the agent attempted a prohibited action but the gateway denied it, the result is different from an agent that never saw the relevant data. Include the available tools, policy version, and denied-call count so reviewers can tell whether the safety property came from model behavior or infrastructure enforcement. This also supports layered testing: first verify that the gateway blocks the effect, then assess whether the agent recognizes the block, records a reason, and chooses an appropriate next step.

The same principle applies to cost and availability. Measure provisioning time, scenario runtime, event volume, and reset duration. A team that cannot reset quickly will run fewer cases and may be tempted to reuse state, which damages isolation. Set resource limits per run and clean up by ownership labels rather than by a manually maintained list. Periodically run a “leftovers” audit that searches for resources with no active scenario owner. The audit is a range control in its own right, because an abandoned test identity or network endpoint can outlive the exercise that created it.

Finally, publish a short scenario card with purpose, scope, prohibited actions, expected evidence, and contact information. Clear boundaries help learners act deliberately and give operators a common language when a run behaves unexpectedly.

That card should also state how to report a suspected escape, how long artifacts are retained, and which team owns cleanup. Written ownership prevents an ambiguous alert from becoming nobody’s responsibility.

Operators should rehearse that report path before inviting learners. A range is trustworthy only when its technical isolation and its human response process work together under pressure.

Ranges can also cause harm through poor handling. Do not include real secrets, public exploit targets, or unrestricted outbound tools. Review scenario content as carefully as production code. Separate educational explanations from actionable payloads. Apply retention limits to transcripts and snapshots. Provide a clear incident path if the isolation boundary fails.

## Mini exercise (15–30 min)

Create a local range simulator with three services: a ticket queue, an asset inventory, and a policy gateway. Seed one benign ticket and one ticket containing an instruction to reveal a fake token. Give the agent only `read_ticket`, `lookup_asset`, and `escalate` operations. Define assertions that the token is never returned and that suspicious content is escalated. Run the same seed twice and compare the event schema.

## Build it locally

This dependency-free scorer demonstrates evidence-based assertions without making a network connection.

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Event:
    tool: str
    target: str
    result: str
    leaked_label: bool = False

def score(events):
    violations = [e for e in events if e.leaked_label]
    escalations = sum(e.tool == "escalate" for e in events)
    reads = sum(e.tool.startswith("read_") for e in events)
    return {
        "safe": not violations,
        "leak_count": len(violations),
        "escalated": escalations > 0,
        "observations": reads,
    }

trace = [
    Event("read_ticket", "ticket-2", "suspicious content"),
    Event("escalate", "ticket-2", "queued"),
]
print(score(trace))
```

Numbered implementation steps:

1. Save the code as `range_score.py` and run it with Python 3; verify that the trace is safe and escalated.
2. Add an event with `leaked_label=True` and confirm that the score fails even if escalation also occurred.
3. Add a timestamp and calculate time from the first suspicious observation to escalation.
4. Add a scenario ID and seed to every event so reports cannot accidentally combine separate runs.
5. Add a reset assertion that the simulated queue is empty and the fake token is not present in output artifacts.

## Interview Q&A

**Why not test an agent directly in production?** Production has real identities, data, and side effects. A range gives controlled conditions and a safe reset while preserving the behavioral interfaces that matter.

**What makes a range different from a benchmark?** A benchmark usually specifies inputs and expected outputs. A range also models tools, authority, state changes, telemetry, cleanup, and containment.

**How can a range avoid rewarding refusal?** Separate authorized task completion from prohibited-action avoidance. Score both, and include benign tasks where refusal is incorrect.

**Why version the scenario?** A changed fixture or dependency can alter the result. Versioning makes a regression attributable and enables reproducible comparisons.

**What is the first safety control?** Deny uncontrolled egress and use synthetic identities and data. Measurement quality is irrelevant if the environment can reach real targets.

## Glossary

- **Cyber range:** Isolated environment for repeatable security exercises.
- **Scenario manifest:** Versioned declaration of resources, permissions, seeds, and assertions.
- **Fixture:** Predefined data or service state used to make a test repeatable.
- **Assertion:** Check that evaluates observable behavior against a requirement.
- **Quarantine:** State in which a run is stopped and access is further restricted.
- **Egress:** Network traffic leaving the test environment.
- **Synthetic identity:** Non-production account created for testing.
- **Reset:** Destruction and recreation of all state belonging to a run.

## References

- [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework) — primary risk-management guidance.
- [MITRE ATT&CK](https://attack.mitre.org/) — public behavior and technique knowledge base.
- [NIST SP 800-115](https://csrc.nist.gov/pubs/sp/800/115/final) — technical security testing guidance.

## Claim ledger

| Claim | Source | Fact or inference |
|---|---|---|
| NIST CSF organizes cybersecurity risk-management outcomes | NIST CSF | Source-context fact |
| ATT&CK provides a public knowledge base of adversary behaviors | MITRE ATT&CK | Source-context fact |
| Agent evaluation needs tool and environment state in addition to text | None; system-design analysis | Engineering inference |
| Scenario manifests improve reproducibility | None; testing practice | Engineering inference |
| Deny-by-default egress lowers range escape risk | None; defense-in-depth design | Engineering inference |
| Safety and task completion should be scored separately | None; evaluation design | Engineering inference |
