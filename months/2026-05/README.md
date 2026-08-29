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
