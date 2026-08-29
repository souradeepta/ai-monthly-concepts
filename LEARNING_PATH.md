# August 2026 learning path

Follow this order; it moves from how to measure AI systems to how to build their data and control planes.

| Order | Lesson | Build skill | Suggested time |
|---:|---|---|---:|
| 1 | [Double-blind evaluations](months/2026-08/01-double-blind-evals.md) | trustworthy benchmarks and threat models | 2 h |
| 2 | [Agent memory](months/2026-08/02-agent-memory.md) | governed retained state and retrieval | 2–3 h |
| 3 | [Late-interaction retrieval](months/2026-08/03-late-interaction-retrieval.md) | precision search under latency/memory limits | 2–3 h |
| 4 | [Agent controls](months/2026-08/04-agent-controls.md) | tool authorization, isolation, and observability | 2–3 h |

## One-week practical route

1. Read each lesson’s introduction and prerequisites; sketch its main diagram from memory.
2. Run the local example and deliberately make one negative test fail.
3. Answer the interview questions aloud in two minutes each.
4. Combine the ideas in a toy local agent: retrieval proposes bounded memory, a policy gateway authorizes tools, logs capture decisions, and tests separate model behavior from control-plane behavior.

## SDE2 outcomes

After this issue, you should be able to explain why benchmark scores need provenance, why memory is a stateful service rather than a prompt dump, when a reranker earns its latency budget, and why a model tool call is not authorization.
