# Checkpoint recovery

Status: draft — expansion and review pending
Sources: [Google DeepMind — 2026-04-23](https://deepmind.google/blog/decoupled-diloco/)

## In one sentence

Checkpoint recovery is the ability to restart work from a verified, compatible snapshot without silently losing, duplicating, or corrupting training progress.

## Draft lesson

A checkpoint must include more than model weights: optimizer state, scheduler, tokenizer, data manifest, random state where needed, source code revision, and a digest. Write it atomically or mark it incomplete; a partially uploaded checkpoint is not a fallback. Restore tests should run regularly, not only during an outage.

The April distributed-training source motivates fault isolation. A recovery playbook should state which island can resume, how it authenticates the artifact store, how it rejects incompatible snapshots, and how it records lineage after restart. Measure recovery time objective, last-known-good age, failed-restore rate, and validation delta after recovery.

## Claim ledger

| Claim | Source | Fact or inference |
|---|---|---|
| The April source presents resilience to local disruptions as a distributed-training goal. | [Announcement](https://deepmind.google/blog/decoupled-diloco/) | Fact, vendor claim |
| Verified restore drills are necessary to establish recoverability. | Systems-design reasoning | Inference |
