# Experiment tracking
Status: draft — expansion and review pending
Sources: [Google DeepMind — AlphaEvolve](https://deepmind.google/blog/alphaevolve-impact/)

## Draft lesson
Every prompt, model, tool, data, policy, evaluator, cost, and output change is an experiment. A trace ID should reconstruct one run from immutable inputs or approved snapshots. Track exceptions and failed runs too; selection bias from only recording winners makes performance claims unreliable.

## Claim ledger
| Claim | Source | Fact or inference |
|---|---|---|
| The source presents iterative algorithmic improvement. | [Source](https://deepmind.google/blog/alphaevolve-impact/) | Fact, vendor claim |
| Versioned traces are required for reproducible operational experiments. | Systems-design reasoning | Inference |
