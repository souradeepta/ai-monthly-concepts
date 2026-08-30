# May 2026 — agent orchestration and AI for discovery

Primary starting points: [Co-Scientist](https://deepmind.google/blog/co-scientist-a-multi-agent-ai-partner-to-accelerate-research/), [AlphaEvolve](https://deepmind.google/blog/alphaevolve-impact/), and [AI-powered pointing](https://deepmind.google/blog/ai-pointer/).

| # | Concept | What an SDE should understand | Build / interview lens |
|---:|---|---|---|
| 1 | **Multi-agent decomposition** | Specialized workers can generate, critique, rank, and synthesize, but coordination adds cost and failure modes. | Say when one agent plus tools beats a swarm. |
| 2 | **Supervisor orchestration** | A supervisor assigns bounded subtasks, carries shared state, and terminates loops. It needs quotas and explicit handoffs. | Design a DAG with retry and cancellation behavior. |
| 3 | **Debate and critique** | Independent critique can expose errors, but correlated models can agree on the same mistake. | Require evidence, diversity, and a final deterministic check. |
| 4 | **Search over programs** | Coding agents can generate candidates, evaluate them against tests/objectives, and iterate. The evaluator defines progress. | Explain why a weak test suite rewards exploitative code. |
| 5 | **Objective functions** | Optimization returns what you measure. Proxy metrics can cause Goodhart-style behavior. | Add guardrail metrics and holdout tests. |
| 6 | **Scientific hypothesis generation** | AI can prioritize hypotheses; experiments and domain experts remain the ground truth. | Track provenance from claim to paper/data/tool result. |
| 7 | **Content provenance** | Users need to know whether content was generated or edited; provenance metadata has limits and can be stripped. | Describe tamper evidence vs. proof of truth. |
| 8 | **Natural interaction** | Pointing, voice, and context reduce UI friction but introduce ambiguous referents and accidental action risk. | Build a confirmation step for destructive commands. |
| 9 | **Structured outputs** | Schemas make downstream parsing reliable, but application code must validate semantics and authorization. | Validate enum values, IDs, ranges, and cross-field invariants. |
| 10 | **Experiment tracking** | Prompt/version/model/data/tool changes are experiments. Capture inputs, outputs, costs, metrics, and exceptions. | Reproduce one run from a trace ID. |

## Capstone prompt

Build a “program improver” over two candidate functions and a test suite. Add a critic that identifies missing tests, then show that the system refuses to choose a candidate without passing a hidden case.

## Speakable summary

“Multi-agent systems buy parallel exploration and specialized roles, but the evaluator, handoff contract, and control plane determine whether that complexity pays off.”

## Articles

1. [Multi-agent decomposition](01-multi-agent-decomposition.md) — draft
2. [Supervisor orchestration](02-supervisor-orchestration.md) — draft
3. [Debate and critique](03-debate-and-critique.md) — draft
4. [Search over programs](04-search-over-programs.md) — draft
5. [Objective functions](05-objective-functions.md) — draft
6. [Scientific hypothesis generation](06-scientific-hypothesis-generation.md) — draft
7. [Content provenance](07-content-provenance.md) — draft
8. [Natural interaction](08-natural-interaction.md) — draft
9. [Structured outputs](09-structured-outputs.md) — draft
10. [Experiment tracking](10-experiment-tracking.md) — draft
11. [Agent state handoffs](11-agent-state-handoffs.md) — draft
12. [Agent budgeting](12-agent-budgeting.md) — draft
13. [Evaluator design](13-evaluator-design.md) — draft
14. [Program sandboxing](14-program-sandboxing.md) — draft
15. [Hypothesis provenance](15-hypothesis-provenance.md) — draft
16. [Human experiment review](16-human-experiment-review.md) — draft
17. [Pointing disambiguation](17-pointing-disambiguation.md) — draft
18. [Agent audit trails](18-agent-audit-trails.md) — draft
19. [Candidate selection](19-candidate-selection.md) — draft
20. [Research reproducibility](20-research-reproducibility.md) — draft
