# Multimodal regression suites

Status: draft — expansion and review pending
Sources: [Google DeepMind — 2026-04-14](https://deepmind.google/blog/gemini-robotics-er-1-6/)

## In one sentence

A multimodal regression suite preserves representative inputs, expected outcomes, timing, and safety assertions so changes in any component can be detected before release.

## Draft lesson

Store replayable fixtures with camera frames, audio chunks, sensor readings, calibration, expected policy decision, and permitted output schema. Redact or synthesize sensitive evidence where retention rules require it. Version fixtures by scenario: good lighting, occlusion, stale frame, conflicting views, interrupted speech, and physical constraint violation.

The April robotics announcement separates evaluation conditions and discusses multiple views and safety constraints. A local regression suite should do the same: label data slice and environment, run deterministic gates before model scoring, and report behavior changes by scenario. A model upgrade is not accepted merely because average success rises if it newly advances after a stale frame or bypasses an abstention condition.

## Claim ledger

| Claim | Source | Fact or inference |
|---|---|---|
| The April release reports multiple evaluation settings and physical-safety-related claims. | [Announcement](https://deepmind.google/blog/gemini-robotics-er-1-6/) | Fact, vendor claim |
| Replayable multimodal fixtures are an effective release control. | Systems-design reasoning | Inference |
