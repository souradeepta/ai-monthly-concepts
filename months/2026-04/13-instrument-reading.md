# Instrument reading

Status: draft — expansion and review pending
Sources: [Google DeepMind — 2026-04-14](https://deepmind.google/blog/gemini-robotics-er-1-6/)

## In one sentence

Instrument reading converts a visual measurement into a typed operational observation with unit, asset identity, range checks, and review behavior.

## Draft lesson

A gauge reading is not just a number. It needs equipment ID, image ID, unit, scale, reading method, capture time, tolerance, and confidence. A service should distinguish `unreadable`, `out_of_range`, `ambiguous_unit`, and `measured`; a guessed value should never be encoded as a normal measurement.

The April robotics source describes analog gauges, sight glasses, pointing, zooming, and code execution in its instrument-reading workflow. In a plant system, bind the result to a known asset registry and deterministic thresholds. Use a human review for alarms with unclear readings, require a fresh capture before actuation, and compare model readings with periodically calibrated reference measurements.

## Claim ledger

| Claim | Source | Fact or inference |
|---|---|---|
| Google DeepMind describes instrument reading that uses visual reasoning, pointing, zooming, and code execution. | [Announcement](https://deepmind.google/blog/gemini-robotics-er-1-6/) | Fact, vendor claim |
| Typed measurement states and deterministic range checks are production controls. | Systems-design reasoning | Inference |
