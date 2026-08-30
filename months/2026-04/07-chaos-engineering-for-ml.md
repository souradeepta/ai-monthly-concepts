# Chaos engineering for ML

Status: draft — expansion and review pending
Sources: [Google DeepMind — 2026-04-23](https://deepmind.google/blog/decoupled-diloco/)

## In one sentence

Chaos engineering for ML deliberately injects realistic faults into data, workers, networks, and dependencies to prove a training or serving system degrades safely and can recover with evidence.

## Draft lesson

An ML pipeline has extra fault modes beyond an HTTP service: a feature distribution can shift, a checkpoint can be incompatible, an accelerator can fail mid-step, and a delayed update can damage a merge. The April distributed-training announcement emphasizes resilience to local disruptions; the engineering response is to test that claim in the actual deployment topology.

Start with a hypothesis and a stop condition. Example: “If one training island loses network for ten minutes, other islands continue, the missing island resumes from a checkpoint, no update is applied twice, and validation quality stays within the defined tolerance.” Inject one failure at a time in a non-production environment. Capture run ID, fault time, affected versions, recovery action, checkpoint lineage, and quality metrics.

Useful experiments include packet loss, clock skew, slow object storage, corrupted input manifests, stale embeddings, unavailable model registry, duplicate queue delivery, and partial checkpoint write. Do not use chaos testing to normalize unsafe behavior: a pipeline that cannot verify a checkpoint should stop rather than silently train from unknown state.

## Claim ledger

| Claim | Source | Fact or inference |
|---|---|---|
| The April source presents fault isolation and hardware resilience as goals of its distributed architecture. | [Announcement](https://deepmind.google/blog/decoupled-diloco/) | Fact, vendor claim |
| Controlled fault injection is an appropriate way to validate recovery behavior. | Systems-design reasoning | Inference |
