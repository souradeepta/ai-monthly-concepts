# March–August 2026 learning path

## Six-month concept maps

- [January](months/2026-01/README.md)
- [February](months/2026-02/README.md)

- [March: agentic foundations](months/2026-03/README.md)
- [April: multimodality and training systems](months/2026-04/README.md)
- [May: orchestration and discovery](months/2026-05/README.md)
- [June: control and reliable deployment](months/2026-06/README.md)
- [July: embodied agents and operations](months/2026-07/README.md)
- [August: deep dives and current concepts](months/2026-08/README.md)

Each map has twenty concepts. The August deep dives are the model for future lesson expansion.
The [extra-ten supplement](months/EXTRA_CONCEPTS.md) brings March–August to twenty concepts each.

## August deep-dive order

March also has an approved deep dive: [Transformer inference](months/2026-03/03-transformer-inference.md).
January now has an approved deep dive: [Tokens and tokenizers](months/2026-01/01-tokens-and-tokenizers.md).
Continue January with [KV caching](months/2026-01/02-kv-caching.md).

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
