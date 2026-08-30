# Sensor freshness

Status: draft — expansion and review pending
Sources: [Google DeepMind — 2026-04-14](https://deepmind.google/blog/gemini-robotics-er-1-6/)

## In one sentence

Sensor freshness makes age and synchronization explicit so a system cannot mistake historical evidence for the current physical world.

## Draft lesson

Every observation should carry capture time, ingest time, source clock, sequence number, and acceptable maximum age. Queue delay, dropped packets, and clock skew can make a technically valid image unsafe for a current decision. Establish a freshness budget per task: a dashboard may tolerate seconds; a grasp verification may tolerate far less.

On expiry, invalidate dependent plans and request a new observation. Log stale rejection rates by camera and network path; a rising rate may be a device or transport incident, not a model-quality regression. Test reordered messages, delayed frames, duplicate frames, and an action that waits behind a long queue.

## Claim ledger

| Claim | Source | Fact or inference |
|---|---|---|
| The April source discusses dynamic multi-camera environments for robotics reasoning. | [Announcement](https://deepmind.google/blog/gemini-robotics-er-1-6/) | Fact, vendor claim |
| Freshness gates are necessary before time-sensitive physical decisions. | Systems-design reasoning | Inference |
