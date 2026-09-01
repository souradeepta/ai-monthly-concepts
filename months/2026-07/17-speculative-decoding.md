# Speculative decoding

Status: emerging

Sources: [Google DeepMind news archive](https://deepmind.google/blog/) (issue discovery context); [Google Research — Accelerating large language model decoding with speculative sampling](https://research.google/blog/accelerating-large-language-model-decoding-with-speculative-sampling/) (primary research context); [Hugging Face assisted generation documentation](https://huggingface.co/docs/transformers/main/en//generation_strategies#speculative-decoding) (implementation context)

## In one sentence

Speculative decoding uses a fast draft model to propose several tokens and a slower target model to verify them in parallel, reducing latency without changing the target model’s accepted distribution when implemented correctly.

## Background: what existed before

Autoregressive language models normally generate one token at a time. The model reads the prompt plus all accepted tokens, computes logits, samples or selects the next token, appends it, and repeats. Even with a key-value cache, each step requires a target-model forward pass. The target may have billions of parameters, so memory bandwidth and kernel launch overhead dominate interactive latency.

Batching improves throughput by serving many requests together, but a single user still waits for sequential decoding. Quantization and optimized attention reduce the cost of each step. Streaming makes waiting feel shorter, yet it does not reduce time to produce the sequence. These techniques are complementary to speculative decoding.

The key observation is that not every token needs a full expensive computation. A smaller draft model can often predict a plausible continuation. The target model can then evaluate a block of proposed tokens in one wider forward pass. Accepted tokens advance the sequence; the first rejected token is sampled from a corrected distribution, and the process repeats.

This is not the same as letting a small model answer and checking it later. The target remains the authority for every accepted token. Correctness depends on a verification rule that accounts for both models’ probabilities, sampling temperature, and rejection behavior.

## What changed and why now

Speculative decoding has moved from a research technique toward production inference because serving costs and interactive latency are limiting agent and chat experiences. Coding assistants, browser agents, and voice interfaces generate many short continuations where a few milliseconds per token accumulate. The issue’s source context indicates active optimization of inference systems; the exact engineering stack remains deployment-specific.

The cited research describes speculative sampling and the implementation documentation exposes assisted-generation interfaces. Those are source-context facts. Choosing a draft model, acceptance length, routing policy, and fallback behavior for a particular service is an engineering inference that must be measured on that service’s prompts.

The practical change is to make decoding a two-model pipeline with observable economics. Operators need draft acceptance rate, target verification time, tokens per target pass, end-to-end latency, and memory overhead. A draft model that is cheap but poorly aligned can lower acceptance and make performance worse. Correctness and speed must therefore be evaluated together.

## Impact on current processing and architecture

The serving request carries two model handles: a target model that defines output behavior and a draft model used only for proposals. The draft proposes up to `k` tokens from the current prefix. The target evaluates those tokens in a vectorized pass, returning probabilities for each position. A verifier accepts the longest prefix that passes the chosen sampling rule. At rejection, it samples one corrected token from the residual distribution and discards later draft tokens.

```mermaid
flowchart LR
  Q[Prompt and accepted prefix] --> D[Fast draft model]
  D --> C[Candidate token block]
  C --> T[Target model verification]
  T --> V{Acceptance test}
  V -->|accept prefix| A[Append accepted tokens]
  V -->|reject at position j| R[Sample corrected token]
  A --> Q
  R --> Q
  A --> O[Stream output]
  R --> O
  classDef input fill:#dbeafe,stroke:#1d4ed8,color:#172554
  classDef model fill:#dcfce7,stroke:#15803d,color:#14532d
  classDef decision fill:#fef3c7,stroke:#b45309,color:#451a03
  class Q,O input
  class D,T,C,A,R model
  class V decision
```

The target can verify a block more efficiently than `k` independent calls because matrix operations process multiple positions together and reuse the prefix cache. The draft still consumes compute and memory, so choose `k` dynamically. Short completions may not amortize the extra model; long, predictable continuations often benefit more. A scheduler can disable speculation for a request when the draft is cold, the target is underutilized, or acceptance has recently collapsed.

Caching becomes two-dimensional. The target cache contains accepted tokens only; draft speculation must not mutate authoritative state until verification. Keep separate cache metadata or clone the relevant suffix. A rejected suffix must be discarded, and a corrected token must be appended to both caches before the next round. Bugs that accidentally retain rejected tokens produce subtle quality and reproducibility failures.

Sampling configuration is part of the contract. Greedy decoding has a simple matching condition, while temperature, top-p, and other filters require a rejection-sampling correction. If the draft uses a different tokenizer, map candidate boundaries carefully or use a compatible tokenizer. Stop sequences and structured-output constraints must be applied during drafting and verification; otherwise the draft may propose tokens the target is not allowed to accept.

## Real-world applications and constraints

An IDE assistant benefits when the draft model predicts routine syntax, boilerplate, or familiar API names. The target still checks each token and preserves its configured safety and style behavior. Measure first-token latency separately from steady-state tokens per second; speculation may help the latter while the draft startup hurts the former.

An agent planner often emits short structured actions. A draft model trained on the same action grammar may achieve high acceptance, but a malformed candidate must be rejected before it reaches a tool adapter. Validate the complete structured object after decoding; token-level acceptance is not semantic authorization.

Voice interfaces have strict latency budgets and variable network conditions. Running draft and target colocated reduces round trips. If the target is remote, transmitting candidate blocks can add overhead and expose prompt data to another service. Encryption, tenancy, and data-processing policy remain requirements even when speculation is an optimization.

Constraints include GPU memory for two models, draft loading time, tokenizer compatibility, changing prompt distributions, and target batching. Acceptance can fall after a model update, new domain, or temperature change. Keep a non-speculative fallback and a feature flag. Cost accounting should include draft GPU time, memory reservation, and extra orchestration—not just target forward passes saved.

## Mental model

Imagine a junior editor drafting several words ahead while a senior editor reviews a whole sentence at once. The senior editor keeps the draft’s prefix only where it agrees with the authoritative style guide. At the first disagreement, the senior supplies the correct word and the junior starts again from that point. The junior accelerates routine work but never overrides the senior.

The distinction is **proposal** versus **authority**. The draft model proposes tokens; the target model defines the distribution. Acceptance rate measures how often proposals are useful, not whether the draft is independently safe or correct. A high rate can coexist with unsafe tool semantics, so downstream validators and policy gates remain necessary.

```mermaid
sequenceDiagram
  participant S as Scheduler
  participant D as Draft model
  participant T as Target model
  participant K as KV-cache manager
  participant C as Client
  S->>D: Request k candidate tokens
  D-->>S: Candidate block and probabilities
  S->>T: Verify block with accepted-prefix cache
  T-->>S: Target probabilities
  S->>S: Apply acceptance and residual sampling
  S->>K: Commit only accepted prefix and correction
  S-->>C: Stream committed tokens
  alt low acceptance or capacity pressure
    S->>D: Disable speculation for next round
    S->>T: Decode one token at a time
  end
```

The system should expose this loop in traces. Record candidate length, accepted length, rejection position, target pass duration, draft duration, and fallback reason. Do not log full sensitive prompts merely to compute these metrics. Aggregates are enough for capacity planning; sampled traces can use redaction and access controls.

## Engineering consequence

Start with an offline corpus representative of production prompts. Compare target-only and speculative outputs under identical random seeds where possible. For stochastic sampling, compare distributions or task metrics rather than exact strings. Include structured generation, stop conditions, long contexts, and prompts that deliberately differ from the draft model’s training distribution.

Tune `k` as a control parameter. Larger blocks offer more potential savings but increase draft work and may waste tokens after an early rejection. A simple adaptive policy can increase `k` after high acceptance and decrease it after repeated rejections. Bound the range and add hysteresis so the policy does not oscillate under noise.

Use a clear service boundary. The scheduler owns request cancellation, deadlines, and fallback. The verifier owns probability correction and cache commits. The model runtime owns kernels and memory. This separation lets a target model update without silently changing the acceptance algorithm. Version the draft-target pair and record both versions in telemetry.

Tables help make the trade-off explicit:

| Condition | Likely choice | Reason |
| --- | --- | --- |
| High draft acceptance, long completion | Enable with larger `k` | Amortize target verification |
| Short response or cold draft | Disable or use small `k` | Avoid startup overhead |
| Target GPU saturated by other batches | Disable speculation | Preserve shared capacity |
| Structured output with strict grammar | Use grammar-aware draft | Prevent unusable candidates |
| Acceptance drops after update | Roll back pair or retune | Protect latency and cost |

## Limits and failure modes

Poor draft alignment can make speculation slower than baseline. A target update may change token probabilities while the draft remains old. Monitor acceptance by route, model pair, language, and prompt class rather than relying on one global average.

Implementation mistakes can change outputs. Reusing rejected cache entries, applying top-p differently in draft and target, or sampling the residual distribution incorrectly violates the intended target distribution. Keep a trusted target-only path for differential tests and audit the verifier as inference-critical code.

Two models double some operational concerns. Memory pressure can trigger eviction or out-of-memory failures. Draft and target failures need independent retry budgets; retrying both can multiply latency. Cancellation must stop speculation promptly and release both caches. A feature flag should allow operators to disable the draft without redeploying the target.

## Build it locally

This low-cost example demonstrates acceptance accounting rather than neural inference. It treats a draft as a list of proposed tokens and accepts matching positions; a real sampler would compare probabilities.

```python
def verify(draft: list[str], target: list[str]) -> tuple[list[str], int]:
    accepted = []
    for proposed, authoritative in zip(draft, target):
        if proposed != authoritative:
            break
        accepted.append(proposed)
    return accepted, len(accepted)

draft = "the quick brown fox".split()
target = "the quick brave fox".split()
accepted, count = verify(draft, target)
print("accepted:", accepted)
print("acceptance rate:", count / len(draft))
```

1. Save it as `verify.py` and run `python3 verify.py`.
2. Add a corrected token after the first mismatch and model the next draft round from the committed prefix.
3. Generate random draft/target sequences and report mean accepted tokens per round.
4. Add a `max_k` policy that shrinks the candidate block after two low-acceptance rounds.
5. Compare a simulated target-only loop with speculative rounds and include draft cost in the timing model.

## Mini exercise (15–30 min)

## Capacity planning and debugging

Benchmark speculation under the same concurrency as the target service. At low concurrency, a draft may improve one request while wasting an otherwise idle target cycle; at high concurrency, the extra draft model can compete for memory and reduce batching efficiency. Measure p50 and tail latency separately, and include queue wait. A faster median with a worse p99 may be unacceptable for an interactive product.

When results regress, inspect the loop in order. First confirm that the target-only baseline still has the expected output and kernel timing. Next check tokenizer boundaries and stopping rules. Then compare draft and target probabilities at the first mismatch. Finally inspect cache commit counters: accepted-prefix length should increase by exactly the number of committed tokens, never by the entire proposed block. These counters often locate a bug faster than reading generated text.

Streaming protocols need a commit boundary. Do not send speculative tokens to a client before verification, because a later rejection would require retracting visible text. Buffer the candidate block internally and stream only committed tokens. For voice or real-time interfaces, this can be balanced with a small verified chunk size; perceived responsiveness is a product metric, but it cannot override output correctness.

Deployment should be gradual. Start with an opt-in route and shadow draft proposals without using them to establish acceptance and overhead. Compare target-only and speculative traces on the same request IDs, then enable a small traffic slice. Roll back when memory pressure, tail latency, output divergence, or error rates exceed a pre-set budget. Keep the target-only path operational throughout the experiment; an optimization that cannot be disabled is an availability risk.

## Mini exercise (15–30 min)

Choose a local text corpus and a deterministic toy target. Create two draft generators: one that copies common prefixes and one that guesses randomly. Measure acceptance, rounds, and simulated work for several `k` values. Plot where speculation wins and identify the acceptance threshold below which fallback is cheaper.

## Interview Q&A

**Does the draft model decide the final output?** No. It proposes; the target verifies and supplies a corrected token at the first rejection.

**Why can a larger draft block hurt?** It costs draft compute and may produce many discarded tokens after an early mismatch.

**What must be tested after changing temperature?** Acceptance behavior and output distribution, because sampling filters affect the verification correction.

**How is production benefit measured?** Track end-to-end latency, target passes per output token, accepted tokens per pass, draft overhead, memory, cost, and fallback rate.

## Glossary

**Acceptance rate:** Accepted draft tokens divided by proposed tokens.

**Draft model:** Smaller, faster model that proposes a candidate token block.

**Residual distribution:** Corrective probability distribution used after a draft rejection.

**Speculative decoding:** Draft-and-verify autoregressive generation.

**Target model:** Authoritative model whose distribution the output must follow.

**KV cache:** Stored attention keys and values reused during decoding.

## References

- [Google Research: Speculative sampling](https://research.google/blog/accelerating-large-language-model-decoding-with-speculative-sampling/) — primary research context.
- [Hugging Face assisted generation](https://huggingface.co/docs/transformers/main/en//generation_strategies#speculative-decoding) — implementation documentation.
- [Google DeepMind news archive](https://deepmind.google/blog/) — issue discovery context.

## Claim ledger

| Claim | Source | Fact or inference |
| --- | --- | --- |
| A draft model can propose tokens for target-model verification. | Google Research | Source-context fact |
| Correct verification can preserve the target sampling distribution. | Google Research | Source-context fact |
| Draft choice and block size must be tuned to workload acceptance. | Lesson synthesis | Engineering inference |
| Speculation does not replace semantic or safety validation for tool actions. | Lesson synthesis | Engineering inference |
