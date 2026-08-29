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
