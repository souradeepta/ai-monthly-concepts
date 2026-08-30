# Training staleness

Status: draft — expansion and review pending
Sources: [Google DeepMind — 2026-04-23](https://deepmind.google/blog/decoupled-diloco/)

## In one sentence

Training staleness is the distance between the state that produced an update and the state that receives it, which asynchronous systems must measure rather than ignore.

## Draft lesson

An update computed from older weights can still be useful, but its age changes the optimization contract. Store source step, receiving step, model digest, data slice, optimizer configuration, and merge time. Set a staleness budget and decide whether to merge, down-weight, quarantine, or discard updates outside it.

Decoupled training islands reduce coordination but create this lifecycle explicitly. Compare validation quality and convergence against a synchronized baseline; “all workers stayed busy” is not sufficient. Test a partitioned island that reconnects with a very old update, an update produced by a different tokenizer, and a duplicate delivery after retry.

## Claim ledger

| Claim | Source | Fact or inference |
|---|---|---|
| The April DiLoCo source describes asynchronous flow between decoupled compute islands. | [Announcement](https://deepmind.google/blog/decoupled-diloco/) | Fact, vendor claim |
| Update age needs explicit merge policy and measurement. | Systems-design reasoning | Inference |
