# September 2026 — concept expansion

Status: **Complete — 20 lessons present, individually validated, runnable examples passing, and month-wide similarity audit passing.**

All twenty article slots are selected from direct, dated September sources. The source-by-source drafting contract, evidence targets, overlap boundaries, and Luna sequence are in [DATA_SOURCES_SPEC.md](DATA_SOURCES_SPEC.md). The candidate archive preserves the research queue and promotion decisions.

## Objective

Expand the repository with twenty source-backed September 2026 lessons for a CS student or SDE2. Each lesson must turn one distinct, high-impact development into an engineering concept: explain the historical baseline, identify what changed in September, connect the change to APIs, state, data/model/tool processing, permissions, queues, tests, cost, latency, or operations, and separate source facts from engineering inference.

The month should extend the January–August learning path rather than repeat it. A candidate is valuable when it adds a new mechanism, failure mode, evaluation practice, deployment constraint, or architecture pattern. A product announcement by itself is not enough.

## Scope and non-goals

In scope:

- announcements, technical reports, papers, benchmarks, incident reports, official documentation, and engineering posts published or materially updated from **2026-09-01 through 2026-09-30**;
- developments with a concrete consequence for building, evaluating, securing, deploying, or operating AI systems;
- primary sources first, with reputable secondary engineering context only when it adds an independent explanation;
- concepts that can support a source-specific 2,400-word lesson and a low-cost local exercise.

Out of scope:

- unverified social-media claims, release-roundup filler, and generic “AI is changing” commentary;
- a vendor capability claim presented as an independently measured fact;
- backfilling older months under a September label;
- a lesson whose only contribution is a renamed version of an existing January–August concept;
- paid APIs, private datasets, or a dependency-heavy example that a reader cannot run locally.

## Collection specification

Run collection in one focused pass, then keep a dated source ledger. Browse only the source pages needed to verify a candidate; do not copy article text into the repository.

### Source feeds to inspect

Start with these primary feeds and official indexes:

- [OpenAI News](https://openai.com/news/)
- [Google DeepMind Blog](https://deepmind.google/blog/)
- [Anthropic News](https://www.anthropic.com/news)
- [Hugging Face Blog](https://huggingface.co/blog)
- [Google Research Blog](https://research.google/blog/)
- [Microsoft Research Blog](https://www.microsoft.com/en-us/research/blog/)
- [Meta AI](https://ai.meta.com/blog/)
- [NVIDIA Technical Blog](https://developer.nvidia.com/blog/)
- [AWS Machine Learning Blog](https://aws.amazon.com/blogs/machine-learning/)
- [arXiv cs.AI, cs.LG, cs.CL, and cs.RO recent lists](https://arxiv.org/list/)
- official benchmark, standards, incident-response, and security project pages when a candidate depends on them.

Use a targeted search only after checking the direct feed. Search combinations should include the month and an engineering noun, for example `September 2026 agent evaluation`, `September 2026 inference serving`, `September 2026 multimodal benchmark`, `September 2026 AI incident`, or `September 2026 model security`. Search results are leads, not evidence.

### Candidate record

Record one row per candidate before selecting a lesson:

| Field | Required content |
|---|---|
| Candidate ID | `sep-01`, `sep-02`, … |
| Working concept | Mechanism, practice, or failure mode; not only a product name |
| Source title and publisher | Exact title and organization/author |
| Publication or update date | ISO date, verified on the source page |
| URL | Direct canonical source URL |
| Source type | Lab post, official docs, paper, benchmark, incident report, or engineering blog |
| September change | One sentence stating what is new this month |
| Baseline | What an engineer would have built or assumed before the change |
| Architecture consequence | Specific effect on processing, state, permissions, queues, latency, cost, or tests |
| Failure/constraint | At least one operational, safety, quality, or reproducibility limitation |
| Primary evidence | Section, figure, result, API behavior, or quoted release fact to verify while drafting |
| Existing overlap | Closest January–August lesson, or `none` |
| Draft decision | `selected`, `watch`, or `reject`, with one reason |

Do not select a candidate when the September change, direct evidence, or distinct engineering consequence is missing.

## Selection rubric

Score each candidate from 0–3 in each category and retain the score plus a short justification:

| Criterion | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| Current-month evidence | No dated source | Date unclear or indirect | Dated primary source | Dated primary source with concrete artifact/result |
| Engineering delta | Product news only | Small API or benchmark detail | Clear architecture or workflow change | New mechanism with broad reusable lesson |
| Distinctness | Duplicates an existing lesson | Mostly overlap | Adds a different layer or failure mode | Clearly new concept and vocabulary |
| Operational depth | No constraints | One shallow caveat | Multiple measurable trade-offs | Failure handling, security, or rollout implications |
| Teachability | No local exercise | Exercise needs paid/private access | Low-cost simulation possible | Runnable example plus meaningful experiment |

Select candidates with at least 10/15, a primary source, and no unresolved factual gap. Prefer a balanced set across model/data processing, agents and tools, evaluation, serving and cost, security and governance, multimodal/embodied systems, and developer workflow. Do not force category balance if the month’s evidence is concentrated elsewhere; record the reason.

## Deduplication against existing lessons

Before selecting a topic, compare its mechanism and failure mode with the existing month indexes and article filenames. A new lesson may build on an older concept only when the September source introduces a materially different processing path or operating constraint. Examples of acceptable separation include a new evaluation protocol versus general evaluation harnesses, or a new serving architecture versus general inference efficiency. Reusing the same introduction, diagram, code pattern, or generic operational appendix is not acceptable.

After drafting the selected batch, run the repository similarity audit. Any finding is a rewrite/review task, not a warning to waive.

## Elaboration contract

Each selected candidate becomes one file named `01-*.md` through `20-*.md` and follows the repository lesson template. The finished lesson must include:

- at least 2,400 substantive, topic-specific words;
- SDE2-friendly introduction and explained prerequisites;
- historical baseline and the September change, with release-specific facts distinguished from inference;
- impact on current data/model/tool processing and realistic applications with constraints;
- two colored Mermaid diagrams: a component/data-flow architecture and a sequence, state, or failure flow;
- a dependency-light runnable Python example;
- numbered local implementation steps for a 15–30 minute exercise;
- interview questions and answers, glossary, references, and a fact/inference claim ledger;
- source-specific failure modes, tests, observability, cost/latency considerations, and security or permission boundaries when relevant.

The monthly README must link all twenty eventual files. Until a lesson exists and passes its checks, its entry remains `planned`; planned entries must not be described as complete.

## Drafting sequence

1. Inspect the existing month indexes and build the September overlap list.
2. Collect and read direct sources; fill the candidate records above.
3. Select and rank at least twenty candidates, keeping additional high-impact items in a watch list when the evidence is strong but the writing slot is full.
4. Freeze the selected concept names, filenames, source URLs, and article order in this README.
5. Elaborate one lesson at a time from its own sources; do not draft from a shared generic outline beyond the required headings.
6. Run the lesson validator with `--run-python`, `git diff --check`, and a word-count check after each lesson.
7. Update this README and `TODO.md` with factual status only. Run the month-wide similarity audit before calling the batch review-ready.

## Acceptance gates

September is complete only when all twenty individual article files exist, every file is linked below, every file passes the learning-content standard, and the month-wide similarity audit passes. A source queue, concept table, or README never counts as an article.

Required checks for each completed lesson:

```text
python3 scripts/validate_lessons.py months/2026-09/<lesson>.md --run-python
git diff --check
```

Required check before monthly review:

```text
python3 scripts/audit_lesson_similarity.py months/2026-09 --fail-on-findings
```

## September article slots

Slots 01–20 are present and pass mechanics, runnable-example, similarity, and substantive review checks. September coverage is complete.

1. [01 — Managed agent harnesses](01-managed-agent-harnesses.md) — complete; validation and review pass
2. [02 — Permission-preserving data agents](02-permission-preserving-data-agents.md) — complete; validation and review pass
3. [03 — Misalignment incident disclosure](03-misalignment-incident-disclosure.md) — complete; validation and review pass
4. [04 — AI-product storage control planes](04-ai-product-storage-control-planes.md) — complete; validation and review pass
5. [05 — Agentic misuse threat intelligence](05-agentic-misuse-threat-intelligence.md) — complete; validation and review pass
6. [06 — Encode–prefill–decode disaggregation](06-encode-prefill-decode-disaggregation.md) — complete; validation and review pass
7. [07 — Trace-shaped LLM benchmarking](07-trace-shaped-llm-benchmarking.md) — complete; validation and review pass
8. [08 — Federated identity propagation](08-federated-identity-propagation.md) — complete; validation and review pass
9. [09 — Item-level benchmark audits](09-item-level-benchmark-audits.md) — complete; validation and review pass
10. [10 — Adaptive visual prompt injection](10-adaptive-visual-prompt-injection.md) — complete; validation and review pass
11. [11 — Jevons paradox in AI](11-jevons-paradox-in-ai.md) — complete; validation and review pass
12. [12 — System One models and typed decisions](12-system-one-models-typed-decisions.md) — complete; validation and review pass
13. [13 — Customer-cloud safety monitoring](13-customer-cloud-safety-monitoring.md) — complete; validation and review pass
14. [14 — Verified high-risk life-sciences access](14-verified-high-risk-life-sciences-access.md) — complete; validation and review pass
15. [15 — Embedded independent evaluation](15-embedded-independent-evaluation.md) — complete; validation and review pass
16. [16 — Precomputed genome-scale model outputs](16-precomputed-genome-scale-model-outputs.md) — complete; validation and review pass
17. [17 — Dropless MoE dispatch at scale](17-dropless-moe-dispatch-at-scale.md) — complete; validation and review pass
18. [18 — Dense-versus-MoE deployment sizing](18-dense-versus-moe-deployment-sizing.md) — complete; validation and review pass
19. [19 — Agent-built, simulation-ready digital twins](19-agent-built-simulation-ready-digital-twins.md) — complete; validation and review pass
20. [20 — Edge agent trajectories](20-edge-agent-trajectories.md) — complete; validation and review pass

## Research ledger

The first-half selection is frozen above. This ledger retains the full research queue; the candidate archive preserves the deferred records for later September selection.

| ID | Working concept | Exact source title / publisher / ISO date | Direct URL | Source type | September change | Score | Existing-overlap check | Decision |
|---|---|---|---|---|---|---:|---|---|
| sep-01 | Managed agent harnesses and portable sandboxes | *Introducing the Agents API* — OpenAI — 2026-09-10 | [source](https://openai.com/index/introducing-the-agents-api/) | Official product/API announcement | Public beta exposed the Codex agent harness, long-running sessions, subagents, and selectable managed or customer-run environments through an API. | 14/15 | Extends July durable execution and February enterprise agent platforms with the runtime/environment boundary. | selected |
| sep-02 | Permission-preserving data agents | *Now everyone can put data to work* — OpenAI — 2026-09-10 | [source](https://openai.com/index/put-data-to-work/) | Official product announcement | ChatGPT Work added a Data agent that uses approved sources and semantic layers while enforcing the connected account's table, row, and column permissions. | 13/15 | Extends January data governance and June policy enforcement points; focus is semantic analytics plus delegated data access. | selected |
| sep-03 | Misalignment incident disclosure lifecycles | *Our framework for reporting model misalignment* — OpenAI — 2026-09-16 | [source](https://openai.com/index/model-misalignment-reporting-framework/) | Lab research / incident-report framework | OpenAI published a disclosure process and six case reports, including triage tracks for observations still under investigation. | 14/15 | Extends June incident response for agents; distinct emphasis is disclosure criteria, investigation state, and external reporting. | selected |
| sep-04 | AI-product online-storage control planes | *Rapidly scaling online storage to serve over 1 billion ChatGPT users* — OpenAI — 2026-09-11 | [source](https://openai.com/index/scaling-storage-one-billion-users-part-one/) | Engineering post | OpenAI documented Habitat's evolution into a storage service with cache, authorization, residency, isolation, and request-shaping layers; it also reports a Rust migration. | 13/15 | Extends January latency and observability lessons; distinct distributed-storage architecture for AI product state. | selected |
| sep-05 | Threat intelligence for agentic misuse and model distillation | *Countering misuse of AI: September 2026* — Anthropic — 2026-09-10 | [source](https://www.anthropic.com/threat-intelligence-report-september-2026) | Threat-intelligence / incident report | The report describes disrupted misuse operations, new evaluations, and alleged unauthorized distillation campaigns targeting Opus-class capabilities. | 13/15 | Extends February threat intelligence and June anomaly triage; source-specific focus is provider-side detection across agentic activity. | selected |
| sep-06 | Customer-cloud safety monitoring | *Developing Enterprise Frontier Safeguards with our customers* — Anthropic — 2026-09-01 | [source](https://www.anthropic.com/news/enterprise-frontier-safeguards) | Official safety architecture announcement | Anthropic announced a phased design that combines zero data retention with misuse detection in customer-controlled cloud infrastructure. | 12/15 | Extends June policy enforcement and January data governance; distinct deployment boundary is safety processing without provider-held enterprise data. | selected for slot 13 |
| sep-07 | Verified high-risk life-sciences access | *Introducing the Life Sciences Verification Program* — Anthropic — 2026-09-17 | [source](https://www.anthropic.com/news/life-sciences-verification-program) | Official safety/access-control announcement | Anthropic introduced organization and project grants with different safeguards, use-case monitoring, and a stated 30-day flagged-activity retention requirement. | 13/15 | Extends June capability scoping and April clinical copilots; distinct mechanism is risk-tiered scientific access and offline pattern monitoring. | selected for slot 14 |
| sep-08 | Embedded independent evaluations | *Partnering with Accenture on embedded evaluation* — Anthropic — 2026-09-18 | [source](https://www.anthropic.com/news/accenture-embedded-evaluation) | Official evaluation-governance announcement | Anthropic announced an evaluator working inside the lab with employee-comparable access to assess training, safeguards, and deployment practice. | 11/15 | Extends March agent evaluation and August double-blind evals; distinct governance model is evaluator access to the development lifecycle. | selected for slot 15 |
| sep-09 | Precomputed genome-scale model outputs | *AlphaGenome Atlas: A predictive map of every possible DNA letter change in the human genome* — Google DeepMind — 2026-09-08 | [source](https://deepmind.google/blog/alphagenome-atlas-a-predictive-map-of-every-possible-dna-letter-change-in-the-human-genome/) | Lab technical/science post | Google DeepMind released a 1-petabyte atlas of precomputed predictions for 9 billion single-nucleotide variants, including an impact score and API access. | 13/15 | Extends May scientific hypothesis generation; distinct concern is serving, ranking, and interpreting a precomputed scientific model-data product. | selected for slot 16 |
| sep-10 | Encode–prefill–decode disaggregation | *When to Use Encode-Prefill-Decode Disaggregation to Accelerate Multimodal Model Serving* — NVIDIA — 2026-09-09 | [source](https://developer.nvidia.com/blog/when-to-use-encode-prefill-decode-disaggregation-to-accelerate-multimodal-model-serving/) | Engineering post | NVIDIA documented Dynamo's independently scalable vision-encode, LLM-prefill, and decode stages and the traffic conditions where the split helps or hurts. | 15/15 | Extends August multimodal serving and July inference efficiency; distinct scheduling and queue topology for media-heavy requests. | selected |
| sep-11 | Multiprocess, trace-shaped LLM benchmarking | *Benchmarking LLM Inference at Scale with AIPerf* — NVIDIA — 2026-09-18 | [source](https://developer.nvidia.com/blog/benchmarking-llm-inference-at-scale-with-aiperf/) | Engineering post / tool announcement | NVIDIA introduced AIPerf as a multiprocess successor to GenAI-Perf with trace replay, configurable arrivals, percentile latency, and telemetry output. | 13/15 | Extends August benchmark reproducibility; distinct issue is preventing the benchmark client from distorting high-concurrency serving measurements. | selected |
| sep-12 | Dropless MoE dispatch at scale | *Accelerating Dropless MoE Training in JAX with NVIDIA Transformer Engine* — NVIDIA — 2026-09-14 | [source](https://developer.nvidia.com/blog/accelerating-dropless-moe-training-in-jax-with-nvidia-transformer-engine/) | Engineering post | NVIDIA described grouped GEMM, expert-parallel dispatch/combine, and communication overlap for training ragged, non-dropped MoE token batches. | 13/15 | Extends April distributed training; distinct failure mode is expert-routing imbalance and all-to-all overhead in dropless MoE. | selected for slot 17 |
| sep-13 | Dense-versus-MoE deployment sizing | *Dense vs. MoE Models: Active Parameters, Throughput, and When to Choose Each* — NVIDIA — 2026-09-15 | [source](https://developer.nvidia.com/blog/dense-vs-moe-models-active-parameters-throughput-and-when-to-choose-each/) | Engineering post | NVIDIA articulated active-parameter compute versus total-parameter memory as a deployment decision, including concurrency and quantization constraints. | 11/15 | Complements sep-12 rather than repeating it: this is serving and capacity selection, not distributed training mechanics. | selected for slot 18 |
| sep-14 | Federated identity propagation for AI platforms | *How to Carry User Identity Across Federated Kubernetes and AI Platforms* — NVIDIA — 2026-09-03 | [source](https://developer.nvidia.com/blog/how-to-carry-user-identity-across-federated-kubernetes-and-ai-platforms/) | Engineering post | NVIDIA documented a central session owner plus stateless regional gateway pattern for delegated identity, refresh, revocation, and audit across data planes. | 14/15 | Extends February agent identity and June revocation; distinct infrastructure is federated Kubernetes/data-plane enforcement. | selected |
| sep-15 | Agent-built, simulation-ready digital twins | *How to Use AI Agents to Prepare 3D Scenes for Simulation* — NVIDIA — 2026-09-16 | [source](https://developer.nvidia.com/blog/how-to-use-ai-agents-to-prepare-3d-scenes-for-simulation/) | Engineering post | NVIDIA described a tool-using workflow that converts Blender scenes into validated OpenUSD inputs with labels, sensors, physics, and preflight checks. | 12/15 | Extends July robot orchestration and April world models; distinct artifact pipeline is simulation-world authoring and validation. | selected for slot 19 |
| sep-16 | Edge agent trajectories as a serving workload | *TensorRT Edge-LLM Completes the MLPerf Edge Agentic Benchmark 6.4x Faster on Jetson AGX Thor* — NVIDIA — 2026-09-16 | [source](https://developer.nvidia.com/blog/tensorrt-edge-llm-completes-the-mlperf-edge-agentic-benchmark-6-4x-faster-on-jetson-agx-thor/) | Engineering post / benchmark result | NVIDIA reported an MLPerf Edge Agentic submission using KV/recurrent-state reuse and tree-based multi-token prediction across multi-turn tool trajectories. | 12/15 | Extends August edge serving and July speculative decoding; distinct workload is stateful tool-use trajectories on constrained hardware. | selected for slot 20 |
| sep-18 | Item-level benchmark construct audits | *BenchMIRT: What are LLM benchmarks actually measuring?* — Ai2 / Hugging Face — 2026-09-01 | [source](https://huggingface.co/blog/allenai/benchmirt) | Research/engineering blog with linked report, data, and code | Ai2 introduced multidimensional item-response analysis to separate latent capabilities within benchmark scores and select informative items. | 13/15 | Extends August benchmark reproducibility; distinct practice is auditing what individual evaluation items measure before trusting an aggregate score. | selected |
| sep-19 | Adaptive visual prompt injection against tool agents | *Repeat-After-Me: Black-Box Adaptive Visual Prompt Injection* — UC Berkeley and FAIR at Meta — 2026-09-03 | [source](https://arxiv.org/abs/2609.04533) | Paper / preprint | The paper introduced a black-box adaptive image injection method evaluated for protected-context disclosure and precise malicious tool calls. | 14/15 | Extends August multimodal prompt injection; the reported adaptive black-box attack and tool-call target strings warrant a source-specific update. | selected |
| sep-20 | Structured self-model memory | *Building a Memory-Driven Agent with NVIDIA NemoClaw* — NVIDIA — 2026-09-04 | [source](https://developer.nvidia.com/blog/building-a-memory-driven-agent-with-nvidia-nemoclaw/) | Engineering post | NVIDIA described a memory design that separates source evidence, human-readable knowledge, SQLite judgments, corrections, and governed execution. | 10/15 | Substantially overlaps August agent memory; the evidence/knowledge/judgment split is promising but needs a sharper distinct lesson boundary. | selected |

## Selected / watch notes

All twenty candidates are selected and now have corresponding article files. Scores assess the strength of an engineering lesson (current-month evidence, engineering delta, distinctness, operational depth, and teachability), not independent verification of vendor-reported capability or performance. The lessons preserve source-specific limitations and do not treat provider claims as independent facts.
