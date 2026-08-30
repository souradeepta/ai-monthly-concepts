# Model artifact provenance

Status: draft — expansion and review pending
Sources: [Google DeepMind model cards — 2026-04-02](https://deepmind.google/models/model-cards/)

## In one sentence

Model artifact provenance connects a running model response to the exact weights, tokenizer, runtime, license, configuration, and evaluation record that produced it.

## Draft lesson

Artifact names are not immutable identity. A release process should resolve an approved model manifest to content digests, source URL, license acceptance, conversion or quantization settings, and test results. An inference gateway records the manifest digest in traces and allows only signed or approved artifacts to load.

The April model-card index provides a starting point for release documentation, but model-card availability does not replace local verification. Quarantine unrecognized artifacts, scan containers, limit model-registry write access, and test rollback under a load that resembles production. When a response is investigated, provenance must answer which executable and weights were active.

## Claim ledger

| Claim | Source | Fact or inference |
|---|---|---|
| The model-card index lists a Gemma 4 April 2026 update. | [Model cards](https://deepmind.google/models/model-cards/) | Fact, vendor index |
| Digest-based manifests improve model release traceability. | Systems-design reasoning | Inference |
