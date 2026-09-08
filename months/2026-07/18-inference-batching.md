# Inference batching

Status: durable

Sources: [NVIDIA Triton Inference Server — 2026-07-29, primary release](https://github.com/triton-inference-server/server/releases/tag/v2.71.0); [NVIDIA — publication date not stated, accessed 2026-09-07, Triton batcher documentation](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/batcher.html); [Hugging Face — publication date not stated, accessed 2026-09-07, optimization documentation](https://huggingface.co/docs/transformers/main/en/llm_tutorial_optimization)

## In one sentence

Inference batching combines compatible requests into shared model executions, improving accelerator utilization while requiring explicit controls for queueing, padding, fairness, memory, and tail latency.

## Prerequisites

Know queueing, tokenization, prefill, decode, KV cache, deadlines, cancellation, and p95 latency. Continuous batching changes the active sequence set between decode rounds; it is not merely waiting for N requests before one static call.

## Background: what existed before

The simplest model service handles one request at a time. It tokenizes input, runs a forward pass, generates output, and returns a response. This is easy to reason about but leaves a GPU idle between requests and pays kernel-launch overhead repeatedly. A static batch fixes the batch size and waits until enough requests arrive; it can increase throughput but makes short requests wait behind long ones.

Language generation adds a second complication. Prefill processes the prompt and decode emits tokens repeatedly. Requests in one batch have different prompt lengths and finish at different times. Padding every sequence to the longest one wastes compute, while removing finished requests changes the active batch. A useful server must schedule work at token and sequence boundaries, not only at HTTP request boundaries.

Dynamic batching collects requests for a short window and forms a batch according to size, shape, priority, and available memory. Continuous batching admits new sequences as others finish. Both require a scheduler that can cancel work, enforce per-tenant quotas, and expose queue time separately from model time.

## What changed and why now

AI products now serve mixed workloads: chat turns, embeddings, tool calls, evaluation jobs, and long-context documents. Agent traffic is bursty and often has strict interactive deadlines. The issue’s source context reflects continued investment in model serving; the exact hardware and runtime are deployment-specific. The architectural lesson is an engineering inference: batching must be treated as a policy and observability problem, not merely a kernel optimization.

The target of optimization has also broadened. Throughput, measured as tokens per second, matters for cost. First-token latency matters for perceived responsiveness. Tail latency matters for user trust and service-level objectives. A scheduler that maximizes average utilization by allowing one long request to monopolize memory can degrade every interactive request.

## What changed this month

NVIDIA’s July 29, 2026 GitHub release for Triton 2.71.0, corresponding to the 26.07 container, provides a direct serving-system anchor for this lesson. The release notes explicitly list enabled PyTorch 2 batching, alongside other backend and frontend changes. That release fact does not prove that every deployment uses continuous batching or that a particular scheduler policy is optimal. The Triton batching documentation supplies the durable primitives; this lesson’s architecture focuses on continuous admission, cache reclamation, cancellation, fairness, and queue policy. Record the policy version with every request so a latency regression can be tied to a scheduler change.

## Impact on current processing and architecture

A serving path typically includes an admission queue, tokenizer, batch scheduler, model runtime, cache manager, and response streamer. The scheduler groups requests with compatible model, adapter, precision, and decoding constraints. It chooses a token budget and reserves memory for key-value caches. The runtime executes prefill or decode work; the streamer emits only committed tokens.

```mermaid
flowchart LR
  C[Clients] --> Q[Admission queues]
  Q --> S[Batch scheduler]
  S --> P[Prefill batch]
  S --> D[Decode batch]
  P --> K[(KV-cache manager)]
  D --> K
  K --> M[Model runtime]
  M --> O[Token stream]
  O --> C
  S --> F[Fairness and quota policy]
  classDef state fill:#dbeafe,stroke:#1d4ed8,color:#172554
  classDef compute fill:#dcfce7,stroke:#15803d,color:#14532d
  classDef guard fill:#fef3c7,stroke:#b45309,color:#451a03
  class C,Q,S,K state
  class P,D,M,O compute
  class F guard
```

Batch compatibility is stricter than “same model.” Requests may have different tokenizers, LoRA adapters, stop conditions, grammars, or privacy domains. Grouping incompatible requests can produce incorrect outputs or leak data through shared caches. Include these attributes in the batching key and make the decision visible in traces.

Padding and packing are central trade-offs. Padding aligns tensors but computes on empty positions. Packing concatenates variable-length sequences with position metadata, reducing waste but increasing implementation complexity. For decode, each active sequence usually contributes one token, so continuous batching can keep the device busy while completions finish at different times. For prefill, chunk long prompts to prevent one request from delaying every other request.

```mermaid
sequenceDiagram
  participant U as Client
  participant Q as Queue
  participant S as Scheduler
  participant G as GPU runtime
  U->>Q: Enqueue prompt with deadline
  Q-->>S: Candidate request
  S->>S: Check compatibility, quota, and memory
  rect rgb(219, 234, 254)
    S->>G: Run prefill microbatch
    G-->>S: KV cache handles
    loop decode rounds
      S->>G: Run active sequences
      G-->>S: Next tokens and finished flags
      S-->>U: Stream committed tokens
      S->>Q: Admit waiting request if capacity exists
    end
    S-->>U: Completion or cancellation reason
  end
  rect rgb(254, 226, 226)
    S->>Q: Expire, cancel, or reject unsafe request
    Q-->>S: Reclaim cache reservation
  end
```

KV-cache memory often becomes the limiting resource. Cache size grows with context length, layers, heads, and precision. Reserve memory before admission and evict only at a defined boundary. Swapping cache blocks to host memory may prevent failure but adds latency. A request that exceeds its budget should be rejected or truncated explicitly, not allowed to trigger an out-of-memory crash that affects every tenant.

## Real-world applications and constraints

Chat serving benefits from continuous batching when many users generate short responses. Use a short batching window to avoid adding visible queue delay. A long-context research request should enter a separate class or receive a prefill budget; otherwise it can monopolize memory. Stream tokens as soon as they are verified and include queue and generation timing in telemetry.

Embedding services can use larger static or dynamic batches because each request has one forward pass and no decode loop. Group by input length buckets to reduce padding, and cap batch bytes rather than only item count. A batch of 1,000 tiny inputs may be cheaper than 100 maximum-length documents.

Evaluation and indexing jobs are throughput-oriented. Route them to a lower-priority queue with a concurrency cap. Fair scheduling prevents background work from starving interactive traffic. If evaluation prompts contain sensitive data, keep them in an isolated model pool or enforce tenant-aware cache boundaries.

Constraints include accelerator memory, kernel shape support, tokenizer CPU cost, network transfer, adapter loading, and cancellation semantics. A request timeout should remove it from future decode rounds and release cache blocks. A cancelled client may still leave an in-flight kernel; the server needs a safe point to reclaim resources.

## Mental model

Think of batching as a bus route. Filling every seat improves efficiency, but delaying the bus until it is full frustrates passengers. Short routes, long routes, priority passengers, and wheelchair access require scheduling rules. The right metric is not passengers per bus alone; it is useful passengers delivered within acceptable waiting time.

The key distinction is **queue latency** versus **compute latency**. Batching can reduce compute cost while increasing queue time. Measure both. Also distinguish throughput from goodput: a server that emits tokens for requests users cancel may show high throughput but poor useful work.

## Engineering consequence

Define service classes with explicit deadlines, maximum prompt and output tokens, priority, and cost budget. Implement weighted fair queuing or a simpler bounded round-robin policy before optimizing kernels. Record admission reason when a request waits: incompatible shape, quota, memory, or deliberate fairness delay.

Use microbatch limits based on tokens and cache bytes, not request count alone. Add backpressure at the edge and return a retry-after signal when admission is closed. A retry should carry an idempotency key for non-idempotent orchestration, but generation requests can usually be safely cancelled and retried if the product accepts different sampling outcomes.

Measure p50, p95, and p99 first-token and inter-token latency; queue time; tokens per GPU-second; padding ratio; cache occupancy; batch size; cancellation; and out-of-memory prevention. Compare homogeneous and mixed workloads. A change that improves mean throughput but worsens p99 should be evaluated against the product SLO, not celebrated automatically.

| Workload | Batching policy | Main risk |
| --- | --- | --- |
| Interactive chat | Short-window continuous batching | Queue delay and tail latency |
| Long-context request | Chunked prefill with reservation | Memory monopolization |
| Embeddings | Length-bucketed dynamic batches | Padding waste |
| Offline evaluation | Large low-priority batches | Starving interactive traffic |

## Limits and failure modes

### Scheduling details that matter in production

Admission should be atomic with cache reservation. If the scheduler accepts a request and discovers later that its context cannot fit, it creates avoidable retries and can starve other tenants. Reserve an estimated cache footprint, then adjust after tokenization; reject with a useful reason when the estimate exceeds a configured ceiling. Keep a small emergency margin for runtime overhead and allocator fragmentation.

Fairness is multidimensional. A tenant may have a request-count limit, token budget, and maximum concurrent cache blocks. Weighted fair queuing can give interactive traffic more service without completely stopping offline work. Add aging so a request waiting behind incompatible shapes eventually receives a scheduling opportunity. Priority must not bypass safety or privacy compatibility checks.

Prefill and decode compete differently. Prefill is compute-heavy and can delay decode tokens; decode is latency-sensitive and often memory-bandwidth-bound. Some runtimes separate them into pools or use prefill chunking. Measure the trade-off with realistic context lengths. A benchmark containing only short prompts can hide the production effect of a single 100,000-token request.

Failures should be explicit. If a worker dies, the scheduler marks the batch uncertain, releases leases after a timeout, and requeues only requests whose output stream was not committed. If a client disconnects, cancellation propagates to the scheduler and cache manager. If a model instance is draining for deployment, stop admitting new work while allowing active sequences to finish or migrate at a defined safe point.

Capacity planning should use demand distributions, not one average. Record burst size, prompt length, output length, concurrency, and cancellation rate. A simple queueing model can estimate required replicas, but validate it with load tests that include correlated bursts and long-tail requests. Keep a low-cost fallback model or a clear overload response; silently increasing queue delay is a poor degradation strategy.

## Operational experiment

Run a local experiment with a mock runtime before changing a production scheduler. Generate interactive requests with short deadlines and offline requests with no strict deadline. Compare three policies: FIFO, shortest-estimated-job-first, and weighted fair queuing. Report p95 first-token delay, completed tokens, deadline misses, and the share of service received by each class. The experiment makes policy trade-offs visible without requiring a large model.

Incorrect compatibility keys can mix adapters or privacy domains. Cache accounting bugs can cause out-of-memory failures. Scheduler starvation can hide behind healthy average latency. Instrument per-tenant and per-class metrics, and test admission under burst and cancellation.

Padding waste grows with length variance. Bucketing reduces waste but may increase waiting for a rare shape. Adaptive windows should have a maximum delay. A model update can change memory use and invalidate previous batch limits; capacity tests belong in deployment gates.

## Continuous batching as a control loop

Continuous batching is easiest to reason about as a repeated control loop: observe arrivals and sequence state, choose a compatible active set, reserve or release cache, execute one decode round, then record what changed. The word “continuous” does not mean that every request is mixed with every other request. It means the set can change at a safe boundary between rounds. A request that finishes leaves immediately, while a newly admitted request joins at its current prefill or decode phase. This removes the static-batch assumption that every sequence has the same remaining length.

The safe boundary is important because a sequence’s key-value cache is stateful. A scheduler may not simply replace a row in a batch while a kernel is using its memory. It must wait for the runtime receipt, mark the old sequence terminal or cancelled, free its blocks, and then attach the new sequence with a compatible model, adapter, tokenizer, and privacy domain. The local simulator below treats one token and one cache slot as a round, but a production runtime may allocate many paged blocks. The invariant is the same: allocation, execution, and reclamation are observable transitions.

Deadline enforcement also needs a precise meaning. A request can miss a first-token deadline while still eventually completing, or it can reach a hard completion deadline with tokens remaining. Record both queue-deadline and completion-deadline misses rather than collapsing them into an “error” count. At the hard boundary, the scheduler should stop admitting more decode work for that request, emit a typed timeout, release its cache, and let the API choose a partial response or a retry. Continuing to generate after the deadline may improve one internal metric while violating the user contract.

Cancellation is a resource event, not just a client-facing status. If the browser disconnects, the request must leave the active set and its cache reservation must be reclaimed even if it has not produced a final token. A late runtime result must be ignored using a sequence or generation identifier; otherwise a cancelled request can reappear in a subsequent batch. The simulator includes a cancellation between rounds so the assertion checks resource release, not only list membership.

Fairness should be measured as service received, not merely number of admissions. Track decoded tokens per tenant, class, and priority; queue delay; deadline misses; and the maximum gap between eligible service opportunities. A high-priority interactive queue can legitimately receive more service, but an offline tenant should not receive zero service indefinitely. Weighted fair queuing, aging, or a bounded priority boost are possible policies. Their weights belong in configuration and traces because changing them changes the product’s latency/cost behavior. Fairness also has a memory dimension: one tenant holding long contexts can consume cache while other tenants wait, even if token counts look balanced.

The scheduler therefore needs a policy version on every batch receipt. When p99 latency rises, operators can distinguish a model-kernel regression from a larger batch delay, a changed deadline policy, a cache leak, or a new tenant mix. Test the policy with burst traces containing short interactive requests, long prefills, cancellations, and incompatible adapters. This is the boundary with speculative decoding: this lesson governs admission, active-set changes, deadlines, cache ownership, and fairness; it does not decide whether one sequence’s tokens were proposed by a draft model.

The July Triton 2.71.0 release is a useful reminder that batching support enters a real serving stack through backend and runtime changes, not only through a diagram in an application design. The release notes identify enabled PyTorch 2 batching for that version; they do not establish that a deployment has the same memory limits, scheduler semantics, or latency profile. Treat the runtime version as part of the batch-policy experiment. Pin it in the benchmark, record its backend configuration, and rerun the workload when upgrading. A release that enables a feature can change the feasible batch shapes without changing the application’s request API.

Dynamic batching and continuous batching solve related but different scheduling problems. A request-oriented dynamic batcher waits for compatible requests and launches a grouped inference call. That is often effective for embeddings or one-shot classification, where every item has one forward pass. Generation adds a stateful decode loop: each sequence has a different remaining length and owns a KV-cache allocation. Continuous batching changes the active set between rounds, so completed sequences can leave and waiting sequences can enter without waiting for the entire original group. The scheduler must therefore coordinate queue admission, cache ownership, and runtime receipts rather than only choose a tensor shape.

Prefill makes the distinction operational. Processing a long prompt can consume substantial compute before any token is streamed, while decode repeatedly touches the cache and is sensitive to inter-token delay. If the scheduler combines an unbounded prefill with latency-sensitive decode work, first-token and inter-token SLOs can fail even though accelerator utilization looks high. Chunked prefill, separate service classes, or a bounded prefill budget are policy options. Measure them with mixed prompt lengths; a benchmark made only of short prompts cannot expose head-of-line blocking caused by a long context.

Admission should be based on a reservation that can be explained. Count prompt tokens, output budget, cache blocks, adapter choice, and service class before placing a request in an active batch. If the reservation does not fit, keep the request queued with a reason and a deadline rather than admitting it and discovering an out-of-memory condition inside the kernel. When a request completes or is cancelled, emit a reclamation receipt and make the freed capacity eligible for the next compatible request. This lets an operator distinguish a full device from a cache leak.

Finally, test the scheduler as a policy under load. Use traces with simultaneous arrivals, different lengths, cancelled clients, a tenant with long contexts, and a low-priority offline queue. Compare throughput with useful completion rate, first-token p95, inter-token p95, deadline misses, cache high-water mark, and service share by tenant. The Triton documentation supplies durable batching concepts; the application still owns compatibility, fairness, privacy, and overload behavior. This is why batching cannot be approved from tokens per second alone.

## Build it locally

This toy scheduler groups requests by model and token budget while respecting a maximum batch size.

```python
from collections import defaultdict, deque

arrivals = deque([
    {"id": "a", "arrival": 0, "tenant": "interactive", "remaining": 3, "deadline": 5},
    {"id": "late", "arrival": 0, "tenant": "offline", "remaining": 5, "deadline": 2},
    {"id": "b", "arrival": 1, "tenant": "offline", "remaining": 1, "deadline": 4},
    {"id": "d", "arrival": 1, "tenant": "offline", "remaining": 4, "deadline": 7},
    {"id": "c", "arrival": 2, "tenant": "interactive", "remaining": 3, "deadline": 9, "cancel_at": 3},
])
active, finished, missed, cancelled = [], [], [], []
service = defaultdict(int)
cache_in_use = 0
max_cache = 0
reclaimed = 0
admitted = 0

for tick in range(9):
    while arrivals and arrivals[0]["arrival"] <= tick:
        item = arrivals.popleft()
        active.append(item)
        admitted += 1
        cache_in_use += 1
    survivors = []
    for item in active:
        if item.get("cancel_at") == tick:
            cancelled.append(item["id"])
            cache_in_use -= 1
            reclaimed += 1
        elif tick >= item["deadline"] and item["remaining"] > 0:
            missed.append(item["id"])
            cache_in_use -= 1
            reclaimed += 1
        else:
            survivors.append(item)
    active = survivors
    active.sort(key=lambda item: (item["deadline"], service[item["tenant"]], item["arrival"]))
    for item in active[:2]:  # one continuous decode round
        item["remaining"] -= 1
        service[item["tenant"]] += 1
        if item["remaining"] == 0:
            finished.append(item["id"])
            cache_in_use -= 1
            reclaimed += 1
    active = [item for item in active if item["remaining"] > 0]
    max_cache = max(max_cache, cache_in_use)
    print("tick", tick, "active", [item["id"] for item in active], "cache", cache_in_use)

total_service = sum(service.values())
fairness_ratio = min(service.values()) / max(service.values())
assert "late" in missed                 # hard deadline removed unfinished work
assert "c" in cancelled                  # cancellation removed a live sequence
assert {"a", "b", "d"}.issubset(set(finished))
assert cache_in_use == 0 and reclaimed == admitted
assert max_cache <= 4 and total_service > 0
assert set(service) == {"interactive", "offline"} and fairness_ratio > 0
```

1. Save as `batch.py` and run `python3 batch.py`.
2. Add deadlines and sort each group by earliest deadline.
3. Track padding waste by comparing the longest item with total tokens.
4. Add a per-tenant quota and reject a batch that exceeds it.
5. Simulate cancellation between rounds and release the cancelled request.

## Implementation exercises

1. Build a Dockerized mock server with interactive and offline queues.
2. Use command-line timing to compare single requests, static batches, and a short dynamic window.
3. Capture only local synthetic traffic with Wireshark and verify that cancellation and retry metadata contain no prompt secrets.
4. Add a Markdown diagram of queue, scheduler, cache, and runtime, then document the latency and throughput trade-off.

## Mini exercise (15–30 min)

Extend the simulator with a fifth request that arrives while `a` is decoding. Track each request’s queue delay, decode rounds, cancellation time, and deadline miss. Compare FIFO with earliest-deadline-first and report whether the policy improved p95 completion time without starving the long request.

## Interview Q&A

**Why does batching improve throughput?** Shared tensor operations and fewer kernel launches use accelerator resources more efficiently.

**Why can batching hurt latency?** Requests wait for a batch window or a long peer, and padding or cache pressure can increase compute.

**What is continuous batching?** Adding and removing sequences between decode rounds so the active batch stays productive as requests finish.

**Which metrics matter?** Queue and compute latency, tail latency, tokens per second, padding, cache occupancy, cancellations, and useful completion rate.

## Glossary

## Deployment checklist

Before enabling a new batching policy, replay a representative trace, verify compatibility keys, and set token and cache ceilings. Load-test bursty arrivals with cancellations and long prompts. Confirm that queue time, model time, cache occupancy, and deadline misses are visible by tenant and service class. Start with a small traffic slice and keep a target-only fallback. Document who can change batch limits, how to drain a replica, and which alert means capacity is unsafe rather than merely slow.

**Dynamic batching:** Forming batches from requests that arrive over time.

**Continuous batching:** Updating the active generation batch between decode rounds.

**KV cache:** Attention state retained for each active sequence.

**Microbatch:** Smaller execution group used to control memory and delay.

**Prefill:** Processing the input prompt before token generation.

## References

- [NVIDIA Triton Inference Server 2.71.0 / 26.07 release](https://github.com/triton-inference-server/server/releases/tag/v2.71.0) — released July 29, 2026; includes the documented PyTorch 2 batching change.
- [NVIDIA Triton batcher documentation](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/batcher.html) — serving and batching context; publication date not stated on the page.
- [Hugging Face optimization documentation](https://huggingface.co/docs/transformers/main/en/llm_tutorial_optimization) — inference optimization context.
- [Google DeepMind news archive](https://deepmind.google/blog/) — issue discovery context.

## Claim ledger
| Claim | Source | Fact or inference |
|---|---|---|
| NVIDIA released Triton Inference Server 2.71.0, corresponding to container 26.07, on July 29, 2026. | [NVIDIA — 2026-07-29](https://github.com/triton-inference-server/server/releases/tag/v2.71.0) | Fact; release metadata |
| The 2.71.0 release notes list enabled PyTorch 2 batching. | [NVIDIA — 2026-07-29](https://github.com/triton-inference-server/server/releases/tag/v2.71.0) | Fact; release note |
| Triton documents dynamic batching controls for inference requests. | [NVIDIA — publication date not stated, accessed 2026-09-07](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/batcher.html) | Fact; documentation scope |
| Continuous batching is a scheduler behavior for variable-length generation, not merely static grouping. | Serving-systems analysis | Engineering inference |
| Queue, cache, cancellation, and fairness policies affect useful throughput and tail latency. | This lesson’s architecture | Engineering inference |
