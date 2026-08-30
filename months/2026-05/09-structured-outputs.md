# Structured outputs
Status: draft — expansion and review pending
Sources: [Google DeepMind — Co-Scientist](https://deepmind.google/blog/co-scientist-a-multi-agent-ai-partner-to-accelerate-research/)

## Draft lesson
Schemas make multi-agent handoffs parseable, but they do not validate truth, ownership, or permission. Give every message a version, required fields, bounded arrays, and an explicit error state. Validate at the producer, queue boundary, and effect owner; authorize from trusted identity and current state.

## Claim ledger
| Claim | Source | Fact or inference |
|---|---|---|
| The source motivates structured multi-agent collaboration. | [Source](https://deepmind.google/blog/co-scientist-a-multi-agent-ai-partner-to-accelerate-research/) | Fact, vendor claim |
| Schema validation and authorization are distinct gates. | Systems-design reasoning | Inference |
