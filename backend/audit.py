"""Append-only audit trail for every agent-loop step.

Records tool calls, delegations, and final outputs so the shop's behavior can
be audited later. The file persists across runs — it is read, appended to,
and rewritten whole each time, but it is never wiped at the start of a run.
"""

from __future__ import annotations

import contextvars
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

AUDIT_PATH = Path(__file__).resolve().parent.parent / "output" / "audit_trail.json"

StepType = Literal["tool_call", "delegation", "final_output"]

# Set by whatever code starts work on a ticket, so every tool call and
# delegation made while that ticket is in progress is tagged automatically.
current_ticket_id: contextvars.ContextVar[int | None] = contextvars.ContextVar(
    "current_ticket_id", default=None
)


def _summarize(value: Any, limit: int = 500) -> Any:
    text = json.dumps(value, default=str)
    if len(text) <= limit:
        return value
    return {"truncated": True, "preview": text[:limit]}


def append_audit(
    agent: str,
    step_type: StepType,
    detail: dict[str, Any],
    ticket_id: int | None = None,
) -> None:
    AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)

    if AUDIT_PATH.exists():
        trail = json.loads(AUDIT_PATH.read_text())
    else:
        trail = []

    trail.append(
        {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "agent": agent,
            "ticket_id": ticket_id if ticket_id is not None else current_ticket_id.get(),
            "step_type": step_type,
            "detail": _summarize(detail),
        }
    )
    AUDIT_PATH.write_text(json.dumps(trail, indent=2))
