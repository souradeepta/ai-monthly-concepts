# Evaluator design
Status: draft — expansion and review pending
Sources: [Google DeepMind — AlphaEvolve](https://deepmind.google/blog/alphaevolve-impact/)

## Draft lesson
An evaluator should be deterministic where possible, isolated from candidate code, versioned, and tested with known bad candidates. Report score, constraints, runtime, and failure reason; never select a candidate solely because it did not crash.
