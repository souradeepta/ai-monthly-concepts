# January 2026 — 20 concepts

Sources: [OpenAI low-latency inference](https://openai.com/index/cerebras-partnership/), [AI adoption and capability overhang](https://openai.com/index/ai-for-self-empowerment/), [AI scientific collaborator](https://cdn.openai.com/pdf/f4b4a5da-b2de-418d-9fcd-6b293e9dc157/oai_ai-as-a-scientific-collaborator_jan-2026.pdf).

1. Tokens and tokenizers — units that drive cost, context, and cache behavior.
2. KV caching — retain attention state to speed autoregressive decoding.
3. Batching — trade request wait time for accelerator utilization.
4. Latency budgets — measure time-to-first-token and total completion separately.
5. Model routing — select model/size by quality, risk, modality, and cost.
6. Quantization — lower weight precision with workload-specific quality checks.
7. Structured output — schemas make generated data consumable, not automatically safe.
8. Function calling — proposals to tools need a policy gateway.
9. RAG — retrieve authorized source context before generation.
10. Embeddings — representations for similarity, clustering, and retrieval.
11. Context engineering — assemble bounded, ordered evidence for a call.
12. Prompt caching — stable prefixes reduce repeated compute.
13. Evaluation harnesses — versioned fixtures plus final-state checks.
14. Hallucination handling — cite sources, validate outputs, and expose uncertainty.
15. Human review — reserve people for high-impact or ambiguous transitions.
16. Observability — traces connect prompt, model, tools, cost, and outcome.
17. AI security — treat model input and tool output as untrusted data.
18. Data governance — define retention, access, deletion, and provenance.
19. Scientific agents — generate hypotheses while experiments remain the oracle.
20. Capability overhang — adoption and workflow design lag technical capability.

## Lessons

1. [Tokens and tokenizers](01-tokens-and-tokenizers.md)
2. [KV caching](02-kv-caching.md)
3. [Batching](03-batching.md)
4. [Latency budgets](04-latency-budgets.md)
5. [Model routing](05-model-routing.md)
6. [Quantization](06-quantization.md)
7. [Structured output](07-structured-output.md)
8. [Function calling](08-function-calling.md)
9. [RAG](09-rag.md)
10. [Embeddings](10-embeddings.md)
11. [Context engineering](11-context-engineering.md)
12. [Prompt caching](12-prompt-caching.md)
13. [Evaluation harnesses](13-evaluation-harnesses.md)
14. [Hallucination handling](14-hallucination-handling.md)
15. [Human review](15-human-review.md)
16. [Observability](16-observability.md)
17. [AI security](17-ai-security.md)
18. [Data governance](18-data-governance.md)
19. [Scientific agents](19-scientific-agents.md)
20. [Capability overhang](20-capability-overhang.md)
