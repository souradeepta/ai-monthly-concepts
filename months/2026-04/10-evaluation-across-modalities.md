# Evaluation across modalities

Status: draft — expansion and review pending
Sources: [Google DeepMind — 2026-04-14](https://deepmind.google/blog/gemini-robotics-er-1-6/)

## In one sentence

Multimodal evaluation checks whether a system reaches the intended outcome under realistic inputs, timing, viewpoints, and safety constraints—not merely whether one model answers a benchmark question.

## Draft lesson

Text accuracy, object detection, and task completion measure different things. A robot may identify a pen correctly yet fail because the frame is stale, the target is unreachable, or success detection advances the plan too early. A voice service may transcribe accurately but feel unusable when interruption latency is high. Build an evaluation matrix covering each component and the end-to-end workflow.

The April robotics announcement reports vendor benchmark comparisons and notes that its single-view and multi-view success-detection evaluations contain different examples and are not comparable. That disclosure is a useful reminder: metric names alone do not establish comparability. Record task definitions, data slices, environment version, camera setup, latency budget, safety policy, and scoring procedure.

Include degraded cases: poor lighting, occlusion, unfamiliar accents, packet loss, stale frames, ambiguous instructions, and missing sensor values. Report false-safe and false-unsafe outcomes separately. For an embodied workflow, a failed stop decision can matter more than a missed optimization. Keep a replayable fixture set and add incidents as regression cases.

## Claim ledger

| Claim | Source | Fact or inference |
|---|---|---|
| The April announcement reports separate single-view and multi-view success-detection evaluations and says their examples are not comparable. | [Announcement](https://deepmind.google/blog/gemini-robotics-er-1-6/) | Fact, vendor claim |
| End-to-end, degraded-condition testing is necessary for multimodal systems. | Systems-design reasoning | Inference |
