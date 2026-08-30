# Multi-view consistency

Status: draft — expansion and review pending
Sources: [Google DeepMind — 2026-04-14](https://deepmind.google/blog/gemini-robotics-er-1-6/)

## In one sentence

Multi-view consistency checks whether observations from different cameras can describe one current world state before a system relies on either view.

## Draft lesson

An overhead camera and wrist camera may disagree because of occlusion, timestamp skew, calibration error, or a moved object. Store camera ID, pose, capture time, calibration version, and object-tracking confidence with every observation. A fusion service should return `consistent`, `conflicting`, or `insufficient_view`, not silently prefer the most fluent interpretation.

The April robotics announcement describes multi-view reasoning for dynamic and occluded environments. In production, use fresh synchronized frames, known coordinate transforms, and a task-specific conflict policy. For a low-risk query, request another frame; for a motion command, stop and route to review. Test one camera blocked, a delayed frame, a shifted camera, and two similar objects seen from different angles.

## Claim ledger

| Claim | Source | Fact or inference |
|---|---|---|
| Google DeepMind describes multi-view reasoning for its April robotics release. | [Announcement](https://deepmind.google/blog/gemini-robotics-er-1-6/) | Fact, vendor claim |
| Cross-view conflicts need explicit state and fallback handling. | Systems-design reasoning | Inference |
