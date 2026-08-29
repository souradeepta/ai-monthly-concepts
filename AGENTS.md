# Contribution rules

## Scope

Teach engineering-relevant AI concepts from the issue month. Prefer primary sources: lab technical posts, official docs, papers, benchmarks, and incident reports. Secondary blogs may add context but cannot be the only evidence.

For each monthly issue, include as many source items as needed to cover distinct, high-impact developments; ten is a learning-map target, not a research cap. Combine primary sources with reputable engineering blogs and impactful peer-reviewed or open-access publications. Mark the source type and do not present vendor claims as independently verified facts.

## Lesson template

```md
# <Concept>
Status: emerging | durable | watch
Sources: [Publisher — YYYY-MM-DD](URL)

## In one sentence
## Background: what existed before
## What changed and why now
## Impact on current processing and architecture
## Real-world applications and constraints
## Mental model
## What changed this month
## Engineering consequence
## Limits and failure modes
## Mini exercise (15–30 min)
## Claim ledger
| Claim | Source | Fact or inference |
```

## Style and budget

- Aim for 1,200–1,800 words when a topic needs depth; define jargon on first use.
- Use systems vocabulary (APIs, state, queues, permissions, tests, cost, latency) before math.
- Separate capability claims from reliability and safety claims.
- Link rather than copy source text; never invent monthly developments.
- Read sources for one concept only. Draft once, then make one fact-check pass. No paid APIs or multi-agent research unless explicitly requested.

## Agent routing

Default to Luna for easy, bounded tasks and Terra for reviews. Use a stronger model only when this would materially improve accuracy or output quality.

## Cold-start workflow

1. Read `MEMORY.md`, `TODO.md`, and the target lesson before acting.
2. Use direct sources already linked in the lesson; browse only to verify or fill a clear gap.
3. Make one scoped edit, run the smallest relevant check, then update `TODO.md`.
4. Keep responses and handoffs terse: outcome, files changed, checks, blocker.

## Learning-content standard

Each lesson must include: SDE2-friendly introduction; explained prerequisites; colored Mermaid diagrams; a runnable low-cost example; numbered local implementation steps; interview Q&A; glossary; references; and a fact/inference claim ledger. Prefer portable diagrams over browser-only animations.

Every new article must also explain the historical baseline, the change introduced by the source, its impact on current data/model/tool processing, and realistic applications with operational constraints. State whether a source claim is a release-specific fact or an engineering inference.
