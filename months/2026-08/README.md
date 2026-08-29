# August 2026 — initial research queue

Status: **research queue, not a claim of comprehensive coverage.**

## Selected concepts

| Concept | Why an engineer should care | Primary starting point |
|---|---|---|
| Double-blind model evaluations | Benchmark leakage can make model scores misleading; secure evaluation design becomes a systems problem. | [Google DeepMind, Aug 27](https://deepmind.google/blog/piloting-the-worlds-first-double-blind-ai-evaluations/) |
| Agent memory | Agents need selective state and retrieval, not an unbounded chat transcript; this affects cost, privacy, and reliability. | [Hugging Face, Aug 18](https://huggingface.co/blog/agents-memory) |
| Multi-vector / late-interaction retrieval | Search can retain token-level vectors, trading index size for precision. | [Hugging Face, Aug 18](https://huggingface.co/blog/multi-vector-embeddings) |
| Cyber-capable agent controls | Tool-using models require sandboxing, authorization, monitoring, and evaluations alongside model capability. | [OpenAI, Aug 7](https://openai.com/index/responding-next-frontier-critical-cyber-capabilities/) |

## Source feeds to check

- [OpenAI News](https://openai.com/news/)
- [Google DeepMind Blog](https://deepmind.google/blog/)
- [Anthropic Newsroom](https://www.anthropic.com/news)
- [Hugging Face Blog](https://huggingface.co/blog)
- [arXiv cs.AI recent](https://arxiv.org/list/cs.AI/recent) — only with code, artifacts, or clear engineering impact.

## Queue discipline

Start with these four, but publish only three to five after source review. A model release alone is not a concept; include it only when it makes a new engineering pattern understandable.

## Lesson filenames

`01-double-blind-evals.md`, `02-agent-memory.md`, `03-late-interaction-retrieval.md`, `04-agent-controls.md`.
