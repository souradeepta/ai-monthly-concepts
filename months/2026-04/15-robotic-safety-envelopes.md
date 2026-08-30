# Robotic safety envelopes

Status: draft — expansion and review pending
Sources: [Google DeepMind — 2026-04-14](https://deepmind.google/blog/gemini-robotics-er-1-6/)

## In one sentence

A robotic safety envelope is deterministic policy around a proposed action: allowed workspace, speed, force, payload, proximity, and emergency-stop behavior.

## Draft lesson

Generative planning can choose a useful next step but cannot be the final enforcement point. The controller needs independent constraints based on the robot configuration and current sensors. A safe action request includes target pose, tool, payload assumption, observation ID, deadline, and caller identity; the controller validates it before trajectory generation.

The April announcement reports vendor safety evaluations and describes handling constraints such as liquids and weight. Engineering teams should independently define hazards for their own site, test constraint violations, and implement fail-safe stop behavior. Keep safety policy versioned and log why a proposal was rejected; never loosen a physical constraint to improve model task completion.

## Claim ledger

| Claim | Source | Fact or inference |
|---|---|---|
| Google DeepMind reports safety-policy and physical-constraint evaluation claims for its release. | [Announcement](https://deepmind.google/blog/gemini-robotics-er-1-6/) | Fact, vendor claim |
| Independent controllers should enforce physical limits. | Systems-design reasoning | Inference |
