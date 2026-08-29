# March 2026 — foundations for agentic AI

This track pairs the month’s research with concepts that make modern systems understandable. Each card is a study unit: explain it, sketch the data flow, then build the local exercise. Primary starting points: [DeepMind on harmful-manipulation evaluations](https://deepmind.google/blog/protecting-people-from-harmful-manipulation/), [DeepMind on AlphaGo’s methods](https://deepmind.google/blog/10-years-of-alphago/), and [OpenAI’s March work report](https://cdn.openai.com/pdf/ChatGPT-and-the-price-of-work_report.pdf).

| # | Concept | What an SDE should understand | Build / interview lens |
|---:|---|---|---|
| 1 | **Transformer inference** | Generation is a loop: tokenize → forward pass → sample a token → append state. KV cache trades memory for avoiding repeated attention work. | Explain why long contexts raise latency/memory; time a toy token loop. |
| 2 | **Context windows** | Context is the model’s temporary working set, not durable memory. Token budgets must reserve room for user input, retrieval, tool results, and output. | Design truncation and summarize-vs-drop rules. |
| 3 | **Tool calling** | A model proposes typed arguments; deterministic code validates, authorizes, executes, and returns bounded output. | State why JSON schema is not an access-control system. |
| 4 | **Agent loop** | Observe → plan → act → observe is a feedback system. State, retries, termination, and side effects make it a distributed-systems problem. | Add a step/cost budget and idempotency key. |
| 5 | **Reinforcement learning + search** | AlphaGo combined learned value/policy estimates with search: a model suggests promising branches while search allocates compute. | Compare greedy decoding, beam search, and environment feedback. |
| 6 | **Evaluation design** | A benchmark is a measurement instrument: define task, data split, grader, metric, variance, and leakage controls before optimizing. | Explain why one aggregate score is insufficient. |
| 7 | **Human-subject evaluation** | Harmful manipulation is not just text classification; outcomes can require controlled studies, consent, and domain-specific measures. | Distinguish model behavior from downstream human effect. |
| 8 | **Prompt injection** | Untrusted text can try to redirect an agent. Treat retrieved pages and tool output as data, never as authority. | Demonstrate a malicious document and show gateway denial. |
| 9 | **Model routing** | Route requests by risk, latency, modality, and cost rather than assuming one model fits all. | Define a fallback when the preferred model is slow or unavailable. |
| 10 | **AI work redesign** | Useful deployment changes workflows: review queues, audit trails, exception handling, and human ownership—not merely chat access. | Describe a human-in-the-loop boundary for one business process. |

## Capstone prompt

Build a local support-draft agent that may search mock tickets but cannot issue refunds. Measure task success, blocked unsafe requests, p95 latency, and human edits. The goal is an evaluation harness, not an impressive prompt.

## Speakable summary

“Modern agentic AI is a probabilistic planner embedded in deterministic systems. I would separate context from memory, model proposals from authority, and task success from safety metrics.”
