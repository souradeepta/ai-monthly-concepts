# April 2026 — multimodality, robots, and training systems

Primary starting points: [Decoupled DiLoCo](https://deepmind.google/blog/decoupled-diloco/), [Gemini Robotics-ER 1.6](https://deepmind.google/blog/gemini-robotics-er-1-6/), and [AI co-clinician research](https://deepmind.google/blog/ai-co-clinician/). Study these as systems patterns, not vendor features.

| # | Concept | What an SDE should understand | Build / interview lens |
|---:|---|---|---|
| 1 | **Multimodal representation** | Text, images, audio, video, and actions must be aligned into representations a model can jointly reason over. | Explain early vs. late fusion and why timestamps/spatial coordinates matter. |
| 2 | **Streaming speech** | Real-time voice requires VAD, chunking, partial transcripts, turn detection, jitter handling, and interruption semantics. | Build a state machine for barge-in and partial output. |
| 3 | **Vision-language-action (VLA)** | A robot stack maps perception and language to actions, but execution still needs calibration, safety envelopes, and feedback. | Separate high-level planning from low-level control. |
| 4 | **Embodied reasoning** | Spatial references, viewpoint changes, and success detection are grounded in sensors and an uncertain physical world. | Name failure modes: occlusion, drift, stale observations, unsafe actuation. |
| 5 | **World models** | A learned predictive model can score imagined action sequences before expensive real execution. | Compare simulation error with a conventional test double. |
| 6 | **Asynchronous distributed training** | Decoupled training islands trade strict synchronization for resilience and lower cross-site communication. | Explain staleness, aggregation, fault recovery, and why convergence must be measured. |
| 7 | **Chaos engineering for ML** | Inject failures—lost workers, slow networks, corrupt inputs—to test whether a training or serving system degrades safely. | Define recovery SLOs and a reproducible fault experiment. |
| 8 | **Open-weight deployment** | Downloadable weights shift responsibility to model serving, quantization, licensing, safety filters, and update operations. | Compare local inference privacy/cost with operational burden. |
| 9 | **Clinical co-pilots** | High-stakes AI should assist a professional with sources, uncertainty, handoff, and auditability; it does not inherit clinical authority. | Explain prospective validation and escalation paths. |
| 10 | **Evaluation across modalities** | A system can ace text metrics yet fail on latency, sensor noise, accessibility, or physical task success. | Define an end-to-end metric suite, not a single benchmark. |

## Capstone prompt

Create a simulated robot task: parse a command, read a JSON “camera” scene, propose a safe action, and stop on uncertain state. Inject one stale sensor frame and prove it is rejected.

## Speakable summary

“Multimodal agents need temporal and physical grounding. I would keep planning, perception, and actuation separately observable, and test the whole feedback loop under noise and failure.”

## Articles

1. [Multimodal representation](01-multimodal-representation.md) — review candidate
2. [Streaming speech](02-streaming-speech.md) — draft
3. [Vision-language-action](03-vision-language-action.md) — draft
4. [Embodied reasoning](04-embodied-reasoning.md) — draft
5. [World models](05-world-models.md) — draft
6. [Asynchronous distributed training](06-asynchronous-distributed-training.md) — draft
7. [Chaos engineering for ML](07-chaos-engineering-for-ml.md) — draft
8. [Open-weight deployment](08-open-weight-deployment.md) — draft
9. [Clinical co-pilots](09-clinical-co-pilots.md) — draft
10. [Evaluation across modalities](10-evaluation-across-modalities.md) — draft
11. [Multi-view consistency](11-multiview-consistency.md) — draft
12. [Success detection](12-success-detection.md) — draft
13. [Instrument reading](13-instrument-reading.md) — draft
14. [Sensor freshness](14-sensor-freshness.md) — draft
15. [Robotic safety envelopes](15-robotic-safety-envelopes.md) — draft
16. [Training staleness](16-training-staleness.md) — draft
17. [Checkpoint recovery](17-checkpoint-recovery.md) — draft
18. [Model artifact provenance](18-model-artifact-provenance.md) — draft
19. [Prospective clinical evaluation](19-prospective-clinical-evaluation.md) — draft
20. [Multimodal regression suites](20-multimodal-regression-suites.md) — draft
