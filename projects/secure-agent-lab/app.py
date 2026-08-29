"""A standard-library teaching lab: bounded memory, retrieval, policy, audit."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
import uuid


MEMORIES = [
    {"id": "m1", "tenant": "acme", "terms": {"refund", "duplicate"},
     "text": "Draft refunds need an idempotency key.", "active": True},
    {"id": "m2", "tenant": "acme", "terms": {"refund", "limit"},
     "text": "Refunds above $50 require approval.", "active": True},
    {"id": "m3", "tenant": "other", "terms": {"refund"},
     "text": "This must never cross the tenant boundary.", "active": True},
]


@dataclass(frozen=True)
class Decision:
    status: str  # allow | deny | needs_approval
    reason: str
    trace_id: str


def retrieve(tenant: str, query: str, limit: int = 2) -> list[dict]:
    """Filter authorization first; rank a tiny lexical corpus second."""
    terms = set(query.lower().split())
    eligible = [m for m in MEMORIES if m["tenant"] == tenant and m["active"]]
    return sorted(eligible, key=lambda m: len(terms & m["terms"]), reverse=True)[:limit]


def authorize(action: str, tenant: str, task_tenant: str, amount: int = 0,
              approved: bool = False) -> Decision:
    trace_id = str(uuid.uuid4())
    if tenant != task_tenant:
        return Decision("deny", "cross-tenant request", trace_id)
    if action not in {"read", "create_draft", "refund"}:
        return Decision("deny", "unknown tool", trace_id)
    if action == "refund" and amount > 50 and not approved:
        return Decision("needs_approval", "refund exceeds $50", trace_id)
    return Decision("allow", "within bounded policy", trace_id)


def run(task: dict) -> dict:
    memories = retrieve(task["tenant"], task["query"])
    decision = authorize(**task["tool"])
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "task_tenant": task["tenant"],
        "selected_memory_ids": [m["id"] for m in memories],
        "decision": asdict(decision),
    }
    return event


if __name__ == "__main__":
    example = {
        "tenant": "acme", "query": "refund duplicate limit",
        "tool": {"action": "refund", "tenant": "acme", "task_tenant": "acme", "amount": 75},
    }
    print(json.dumps(run(example), indent=2))
