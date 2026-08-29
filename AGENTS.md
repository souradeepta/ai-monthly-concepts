# Contribution rules

## Scope

Teach engineering-relevant AI concepts from the issue month. Prefer primary sources: lab technical posts, official docs, papers, benchmarks, and incident reports. Secondary blogs may add context but cannot be the only evidence.

## Lesson template

```md
# <Concept>
Status: emerging | durable | watch
Sources: [Publisher — YYYY-MM-DD](URL)

## In one sentence
## Mental model
## What changed this month
## Engineering consequence
## Limits and failure modes
## Mini exercise (15–30 min)
## Claim ledger
| Claim | Source | Fact or inference |
```

## Style and budget

- 500–900 words; define jargon on first use.
- Use systems vocabulary (APIs, state, queues, permissions, tests, cost, latency) before math.
- Separate capability claims from reliability and safety claims.
- Link rather than copy source text; never invent monthly developments.
- Read sources for one concept only. Draft once, then make one fact-check pass. No paid APIs or multi-agent research unless explicitly requested.

## Agent routing

Default to Luna for easy, bounded tasks and Terra for reviews. Use a stronger model only when this would materially improve accuracy or output quality.
