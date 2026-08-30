# Agent state handoffs
Status: draft — expansion and review pending
Sources: [Google DeepMind — Co-Scientist](https://deepmind.google/blog/co-scientist-a-multi-agent-ai-partner-to-accelerate-research/)

## Draft lesson
Agent handoffs need a durable task ID, input digest, claimed result, evidence links, owner, expiry, and terminal state. Conversation text is not reliable shared state. A receiving worker revalidates scope and permissions before using a handoff.
