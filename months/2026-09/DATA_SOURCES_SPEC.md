# September 2026 — data-sources and lesson implementation specification

Status: **implementation specification only — no September lesson files exist.**

This is the source-specific handoff for Luna. It freezes the first ten September lessons while preserving the other ten researched candidates in [CANDIDATE_ARCHIVE.md](CANDIDATE_ARCHIVE.md). A source URL, this specification, or a planned README link is not a completed lesson.

## Operating contract

For one lesson at a time, Luna must read the direct primary source below before drafting. Follow its internal links only when they establish an API behavior, report methodology, benchmark metric, or security boundary needed by that one lesson. Do not use a product announcement to make an independently verified performance, security, or reliability claim. Attribute such statements to its publisher or authors.

Each lesson must use the repository's lesson headings, contain at least 2,400 substantive topic-specific words, and define jargon on first use. The audience is a CS student/SDE2: start from interfaces, state, queues, permissions, tests, cost, latency, and operations before introducing math. Do not share prose, diagrams, generic operational appendices, or code among September lessons.

## Frozen queue and direct-source evidence plan

| Queue | Candidate | Final lesson filename | Direct primary source | Date | Source type | Evidence Luna must extract before drafting |
|---:|---|---|---|---|---|---|
| 01 | sep-01 — Managed agent harnesses and portable sandboxes | `01-managed-agent-harnesses.md` | [Introducing the Agents API — OpenAI](https://openai.com/index/introducing-the-agents-api/) | 2026-09-10 | Official product/API announcement | Public-beta status; session creation contract; managed vs customer/VPC environment choice; long-session context management; tool search/programmatic calls; subagent lifecycle; pricing or availability caveats. |
| 02 | sep-02 — Permission-preserving data agents | `02-permission-preserving-data-agents.md` | [Now everyone can put data to work — OpenAI](https://openai.com/index/put-data-to-work/) | 2026-09-10 | Official product announcement | Approved connector and semantic-layer role; administrator connection/role controls; source-account table/row/column permission enforcement; evidence/dashboard/action flow; which actions require approval. |
| 03 | sep-03 — Misalignment incident disclosure lifecycles | `03-misalignment-incident-disclosure.md` | [Our framework for reporting model misalignment — OpenAI](https://openai.com/index/model-misalignment-reporting-framework/) | 2026-09-16 | Lab research / disclosure framework | Criteria for a reportable observation; stated six initial reports; triage/investigation state; publication timing before complete explanation or mitigation; report contents; stated limits of the first set. |
| 04 | sep-04 — AI-product online-storage control planes | `04-ai-product-storage-control-planes.md` | [Rapidly scaling online storage to serve over 1 billion ChatGPT users — OpenAI](https://openai.com/index/scaling-storage-one-billion-users-part-one/) | 2026-09-11 | Engineering post | Habitat request path and its cache, authorization, residency, isolation, encryption, request-shaping, routing, and change-data-capture layers; library-to-service rationale; deployment fan-out failure; provider-reported scale figures; explicitly reported migration decisions. |
| 05 | sep-05 — Threat intelligence for agentic misuse and model distillation | `05-agentic-misuse-threat-intelligence.md` | [Detecting and countering misuse of AI: September 2026 — Anthropic](https://www.anthropic.com/threat-intelligence-report-september-2026) | 2026-09-10 | Provider threat-intelligence report | Report scope and observation window; case-study versus prevalence distinction; detection, disruption, account enforcement, and indicator-sharing process; stated agentic-misuse and illicit-distillation findings; what the report cannot independently establish. |
| 06 | sep-10 — Encode–prefill–decode disaggregation | `06-encode-prefill-decode-disaggregation.md` | [When to Use Encode-Prefill-Decode Disaggregation to Accelerate Multimodal Model Serving — NVIDIA](https://developer.nvidia.com/blog/when-to-use-encode-prefill-decode-disaggregation-to-accelerate-multimodal-model-serving/) | 2026-09-09 | Engineering post | Aggregated, colocated, and disaggregated encoder topologies; stage boundaries and embedding transfer; traffic/workload conditions; head-of-line blocking explanation; TTFT, end-to-end latency, and goodput definitions; vendor benchmark configuration and caveats. |
| 07 | sep-11 — Multiprocess, trace-shaped LLM benchmarking | `07-trace-shaped-llm-benchmarking.md` | [Benchmarking LLM Inference at Scale with AIPerf — NVIDIA](https://developer.nvidia.com/blog/benchmarking-llm-inference-at-scale-with-aiperf/) | 2026-09-18 | Engineering post / tool announcement | Why a client becomes a measurement bottleneck; multiprocess generator/aggregator architecture; arrival distributions and trace replay; endpoint support; TTFT, inter-token latency, request latency, output throughput, percentiles, and telemetry; whether a metric is tool output versus a general benchmark result. |
| 08 | sep-14 — Federated identity propagation for AI platforms | `08-federated-identity-propagation.md` | [How to Carry User Identity Across Federated Kubernetes and AI Platforms — NVIDIA](https://developer.nvidia.com/blog/how-to-carry-user-identity-across-federated-kubernetes-and-ai-platforms/) | 2026-09-03 | Engineering post | Central session owner, stateless regional gateway, `/gateway/userinfo`, and Redis/TTL roles; OIDC and trusted-header boundary; refresh/logout/revocation flow; mTLS or workload identity; header stripping; fail-closed versus bounded cached-validation decision. |
| 09 | sep-18 — Item-level benchmark construct audits | `09-item-level-benchmark-audits.md` | [BenchMIRT: What are LLM benchmarks actually measuring? — Ai2 on Hugging Face](https://huggingface.co/blog/allenai/benchmirt) | 2026-09-01 | Research/engineering post, with linked [report](https://allenai.org/papers/benchmirt), [data](https://huggingface.co/collections/allenai/benchmirt), and [code](https://github.com/allenai/BenchMIRT) | Unit of analysis (model-by-item response matrix); multidimensional item-response theory; item difficulty/discrimination; stated examples where aggregate scores confound constructs; selection of informative items; identifiability, sample-size, and interpretation limits. |
| 10 | sep-19 — Adaptive visual prompt injection against tool agents | `10-adaptive-visual-prompt-injection.md` | [Repeat-After-Me: Black-Box Adaptive Visual Prompt Injection — arXiv](https://arxiv.org/abs/2609.04533) | 2026-09-03 (v1; revised 2026-09-15) | Research preprint | Threat model, attacker access, benign-prompt condition, adaptive loop, protected-context/tool-call targets, reported model set and ASR methodology, stated transfer result, and authors' proposed defenses. Do not reproduce attack payloads or operational exploit steps. |

### Per-source research rules

1. Record exact title, publisher, ISO date, canonical URL, and source type in `Sources:` and `References`.
2. Make a short private drafting note with the evidence targets above. Do not paste source text into a lesson; summarize and link it.
3. Mark source-specific factual claims as “OpenAI states,” “Anthropic reports,” “NVIDIA’s experiment reports,” “Ai2 introduces,” or “the paper’s authors report” where appropriate.
4. Use general systems knowledge only to explain the mechanism, and label design recommendations as engineering inference. If a primary source does not support a number, remove the number.
5. For the AIPerf and NVIDIA EPD posts, treat the page's AI-generated summary as a navigation aid, then corroborate important claims in the body, linked code, or documentation. For the preprint, label results as preprint-author results, not a completed security assessment.

## Candidate boundaries and overlap controls

| September lesson | It teaches | Do not repeat | Required differentiator |
|---|---|---|---|
| 01 | Harness/environment API boundary for durable, tool-using agents | July durable execution; February stateful runtimes and enterprise agent platforms | Compare managed and customer-run sandboxes: file/secrets persistence, isolation, portability, cold start, and incident ownership. |
| 02 | Delegated analytics against governed semantic data | January data governance; June policy-enforcement points | Follow one natural-language question through semantic resolution, permission filtering, evidence, dashboard, and approved action; do not make it a generic RBAC lesson. |
| 03 | External disclosure lifecycle for unexpected model behavior | June incident response for agents | Cover reportability, investigation state, release criteria, public correction, and evidence boundaries—not runtime containment or generic playbooks. |
| 04 | Shared online-storage control plane for AI product state | January latency budgets and observability | Explain library-to-service migration and storage governance layers; do not retell cache basics without request routing, authorization, and deploy fan-out. |
| 05 | Provider-side threat intelligence as a detection/disruption data product | February threat intelligence; June anomaly triage; July cyber evaluation | Focus on evidence collection, classification, enforcement, indicator sharing, and uncertainty. Do not turn cases into offensive instructions or claim prevalence. |
| 06 | Queue topology for multimodal inference stages | July inference efficiency/speculative decoding; August edge serving | Explain encode versus prefill versus decode resource isolation and cross-stage transfer; not generic batching or model quantization. |
| 07 | Benchmark-client fidelity under concurrent, bursty load | August benchmark reproducibility | Make the benchmark generator part of the system under test: arrival process, trace replay, client saturation, and telemetry. Do not duplicate manifest/provenance prose. |
| 08 | User-principal propagation across federated control and data planes | February agent identity; June agent identity and revocation | Trace one user across gateway/session store/cluster service with refresh/logout/revocation. Do not make agent principals or approval tokens the topic. |
| 09 | Construct validity audit at the individual benchmark-item level | August benchmark reproducibility; March agent evaluation | Explain what an item discriminates and how aggregate scores obscure constructs; do not repeat generic reproducibility manifests or leaderboard leakage. |
| 10 | Adaptive visual injection risk against multimodal tool agents | August multimodal prompt injection; March secure prompt injection; July browser sandboxing | Explain adaptive black-box optimization and precise tool-call target risk at a defensive, non-actionable level; center provenance, modality isolation, authorization, and regression tests. |

Before every draft, run a narrow `rg` search against the named predecessor lessons and compare the planned diagram, local code, and exercise. The wording, visual flow, and runnable example must be specific to the September mechanism. The month-wide similarity audit is mandatory after a reviewed batch.

## Required lesson shape

Every resulting article needs the standard headings: `In one sentence`, `Background`, `What changed`, `Impact on current processing`, `Real-world applications`, `Mental model`, `What changed this month`, `Engineering consequence`, `Limits and failure modes`, `Mini exercise`, and `Claim ledger`, plus the validator-required `Build it locally`, `Interview Q&A`, `Glossary`, and `References` sections.

Each lesson must have these distinct deliverables:

- two colored Mermaid diagrams: (1) component/data flow and (2) sequence, state transition, or failure flow; define and use named `classDef` colors;
- a dependency-free, safe Python example that executes with `python3`, makes its assertion(s), and produces useful output;
- numbered local implementation steps that extend that exact example in 15–30 minutes;
- at least four interview questions with direct answers and a topic-specific glossary;
- a claim ledger with direct source URL or named engineering basis on every nontrivial claim.

Suggested safe example boundaries: a sandbox-policy selector (01), row/column filter simulator (02), incident-state transition validator (03), routed-cache control plane simulator (04), indicator-redaction pipeline (05), staged-request scheduler (06), synthetic-arrival benchmark driver (07), token/header validation gate (08), item-response matrix analyzer without fitting claims (09), and image-origin/tool-authorization policy regression test (10). These are examples to build, not shared templates; each must be written separately.

## Fact, inference, and safety rules

| Claim class | How to write it | Example |
|---|---|---|
| Release-specific fact | Attribute it and cite the direct source. | “OpenAI states that the API was in public beta on September 10, 2026.” |
| Vendor/author measurement | Attribute the experiment, configuration, and limitation; do not generalize. | “NVIDIA reports this result for its described EPD workload; it is not a universal latency guarantee.” |
| Security incident/case allegation | Attribute it to the reporting organization; distinguish observed activity, attribution, enforcement, and impact. | “Anthropic reports it disrupted the described activity.” |
| Engineering inference | Mark as inference and ground it in an explained system property. | “A central session store can increase blast radius; teams should choose fail behavior explicitly.” |
| Defensive safety guidance | Keep operationally useful for defenders but non-actionable for attackers. | Describe input provenance and tool authorization tests, not a visual-payload construction recipe. |

Never turn the following into facts: customer testimonials, provider scale/cost/reliability numbers, benchmark performance, model security, threat-actor identity, or claims that a control “prevents” a class of harm. Discuss residual risk, false positives/negatives, outages, replay, stale state, and observability for the topic instead.

## Luna sequencing and checks

1. Start with one frozen queue item; read `MEMORY.md`, `TODO.md`, this specification, the matching README row, the direct source, and only the named overlap lessons.
2. Create only the mapped article file. Keep its README entry `planned` until it passes the per-file checks; do not advance the month to complete.
3. Draft once from source-specific notes, then fact-check every number, date, proper noun, and result against the direct source. Add fact/inference labels while editing.
4. Run the exact per-file checks:

   ```text
   python3 scripts/validate_lessons.py months/2026-09/<filename> --run-python
   git diff --check
   ```

5. Update `TODO.md` only with factual draft/check status. Do not change the archive, promote slots 11–20, or label September complete.
6. After a reviewed multi-file batch—and before any monthly push—run:

   ```text
   python3 scripts/audit_lesson_similarity.py months/2026-09 --fail-on-findings
   ```

The validator requires each supplied file to have 2,400 words, two Mermaid fences, an extractable runnable Python fence, numbered steps, and the required headings. When pointed at a month directory, it also requires exactly 20 numbered article files. Therefore, run it against individual September lesson files during this first-half implementation phase; the month-directory validation belongs only after all twenty slots have articles.

## Completion boundary

The ten frozen files are a mid-month queue, not a new definition of completion. Slots 11–20 remain planned until a later source-review decision promotes deferred candidates from the archive. September can be called complete only when all twenty individual lessons exist, are linked by the README, meet the learning-content standard, and pass the month-wide similarity audit.
