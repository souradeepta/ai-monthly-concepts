# June 2026 — control, safety, and reliable deployment

Primary starting points: [Google DeepMind’s AI Control Roadmap](https://deepmind.google/blog/securing-the-future-of-ai-agents/) and [multi-agent safety research](https://deepmind.google/blog/investing-in-multi-agent-ai-safety-research/).

| # | Concept | What an SDE should understand | Build / interview lens |
|---:|---|---|---|
| 1 | **Defense in depth** | Alignment, sandboxing, authorization, monitoring, and response are overlapping layers; none is a single safety switch. | Map which layer catches each failure. |
| 2 | **Agent control** | Treat capable agents as potentially misaligned at runtime: observe plans/actions and limit authority incrementally. | Explain prevention vs. after-the-fact remediation. |
| 3 | **Monitoring coverage and recall** | Coverage asks how much traffic is observed; recall asks how much harmful behavior is caught. Both can fail independently. | Choose metrics for a policy-monitoring rollout. |
| 4 | **Synchronous intervention** | High-impact actions need a real-time gate before execution; asynchronous review suits reversible, low-impact work. | Classify actions by irreversibility and blast radius. |
| 5 | **Chain-of-thought limits** | Visible reasoning is a useful signal, not a complete truth source; models may omit, distort, or optimize around observation. | Use behavior and tool traces as independent evidence. |
| 6 | **Agent identity** | Services need workload identity, scoped capabilities, expiry, and revocation—not shared static keys in prompts. | Design a short-lived token for one tool action. |
| 7 | **Multi-agent protocols** | Independent agents need authentication, commitments, reputation, rate limits, and dispute handling. | Explain why a message is not proof of intent. |
| 8 | **Sandbox/testbed design** | A realistic, reproducible environment lets you measure interactions without exposing production systems. | Build fake APIs with seeded data and failure injection. |
| 9 | **Incident response for agents** | Stop runs, revoke credentials, preserve traces, assess impact, and patch the boundary before resuming. | Write a kill-switch runbook. |
| 10 | **Safety cases** | A deployment argument should state claims, evidence, assumptions, and residual risk—not simply say “we tested it.” | Produce a one-page safety case for a draft-only agent. |

## Capstone prompt

Extend the secure-agent lab with a monitor that flags cross-tenant proposals, a circuit breaker after repeated denials, and a JSONL incident trace. Test that a “halt” revokes future actions.

## Speakable summary

“Reliable agent deployment is a control problem: bound authority, observe behavior, intervene before irreversible effects, and make residual risk explicit.”

## Articles

1. [Defense in depth](01-defense-in-depth.md) — draft
2. [Agent control](02-agent-control.md) — draft
3. [Monitoring coverage and recall](03-monitoring-coverage-and-recall.md) — draft
4. [Synchronous intervention](04-synchronous-intervention.md) — draft
5. [Chain-of-thought limits](05-chain-of-thought-limits.md) — draft
6. [Agent identity](06-agent-identity.md) — draft
7. [Multi-agent protocols](07-multi-agent-protocols.md) — draft
8. [Sandbox and testbed design](08-sandbox-testbed-design.md) — draft
9. [Incident response for agents](09-incident-response-for-agents.md) — mechanics pass complete; substantive review pending
10. [Safety cases](10-safety-cases.md) — mechanics pass complete; substantive review pending
11. [Capability scoping](11-capability-scoping.md) — mechanics pass complete; substantive review pending
12. [Policy enforcement points](12-policy-enforcement-points.md) — mechanics pass complete; substantive review pending
13. [Anomaly triage](13-anomaly-triage.md) — mechanics pass complete; substantive review pending
14. [Approval boundaries](14-approval-boundaries.md) — mechanics pass complete; substantive review pending
15. [Revocation](15-revocation.md) — mechanics pass complete; substantive review pending
16. [Agent rate limits](16-agent-rate-limits.md) — mechanics pass complete; substantive review pending
17. [Agent containment](17-containment.md) — mechanics pass complete; substantive review pending
18. [Audit evidence](18-audit-evidence.md) — mechanics pass complete; substantive review pending
19. [Control evaluations](19-control-evaluations.md) — mechanics pass complete; substantive review pending
20. [Residual risk](20-residual-risk.md) — mechanics pass complete; substantive review pending
