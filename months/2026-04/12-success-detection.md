# Success detection

Status: draft — expansion and review pending
Sources: [Google DeepMind — 2026-04-14](https://deepmind.google/blog/gemini-robotics-er-1-6/)

## In one sentence

Success detection is a separate verification decision: did the intended final state happen, with enough current evidence to advance the workflow?

## Draft lesson

Planning an action and observing success are different problems. A robot can issue “place pen in holder” and still fail because the pen bounced out, the holder was occluded, or another object was moved. Define success as a predicate over observable state, such as object identity, containment relation, timestamp, and confidence. Persist the action ID and post-action observations that satisfied the predicate.

The April source calls success detection an engine of autonomy and discusses single- and multi-view evaluations. Treat completion as a safety-sensitive state transition: false completion can cause the next action to damage a task, while false incompletion may trigger duplicate work. Include a retry limit, re-observation path, and human escalation.

## Claim ledger

| Claim | Source | Fact or inference |
|---|---|---|
| The April announcement describes success detection as important for choosing whether to retry or progress. | [Announcement](https://deepmind.google/blog/gemini-robotics-er-1-6/) | Fact, vendor claim |
| A success predicate should be independent from an action proposal. | Systems-design reasoning | Inference |
