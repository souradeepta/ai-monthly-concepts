# Open-weight deployment

Status: draft — expansion and review pending
Sources: [Google DeepMind model cards — 2026-04-02](https://deepmind.google/models/model-cards/)

## In one sentence

Open-weight deployment moves more of the model lifecycle into an engineering team's environment: artifact verification, serving, hardware fit, update policy, access control, and incident response.

## Draft lesson

Downloading weights does not turn a model into a static library. A deployment must identify the exact artifact digest, license, tokenizer, runtime, quantization method, prompt or policy version, and model-card limitations. Put these values in an immutable release manifest. A response trace should say which manifest produced it.

The April model-card index lists Gemma 4 with an April 2 update. That index entry is a source fact; local serving performance, safety, and cost are deployment-specific. Teams can gain data locality and control, but they also own GPU capacity, autoscaling, patching, abuse controls, evaluation, and rollback. An unreviewed community quantization may alter output behavior and cannot be assumed equivalent to the original artifact.

Begin with an internal, low-risk read-only workload. Enforce authentication at the inference gateway, isolate tenant data, cap request and generation sizes, and log redacted operational metadata. Test cold start, out-of-memory recovery, malicious prompts, model-load failure, and rollback to a known manifest.

## Claim ledger

| Claim | Source | Fact or inference |
|---|---|---|
| The Google DeepMind model-card index lists Gemma 4 with an April 2, 2026 update. | [Model cards](https://deepmind.google/models/model-cards/) | Fact, vendor index |
| Local deployment transfers serving and governance responsibility to the operator. | Systems-design reasoning | Inference |
