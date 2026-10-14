"""FastAPI backend for the Campus Customs dashboard.

Every shop-fact read and write goes through the MCP server — the same
source of truth the agent team uses — so the dashboard and the agents never
see different realities. Agents can only recommend a payment; only the
/payments/approve route (triggered by a human clicking Approve) actually
calls the MCP server's record_payment tool and moves cash.
"""

from __future__ import annotations

# This file is started directly as `uvicorn main:app` from inside backend/,
# so Python loads it as a top-level module with no package context — but it
# still uses the package's relative imports (`.audit`, `.boss_agent`, ...) so
# that every module resolves to the same single "backend.*" identity whether
# the app is started this way or imported as `backend.main` from the project
# root. This shim gives it that package context before the imports run.
if __package__ in (None, ""):
    import sys as _sys
    from pathlib import Path as _Path

    _sys.path.insert(0, str(_Path(__file__).resolve().parent.parent))
    __package__ = "backend"

import json
import shutil
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .audit import AUDIT_PATH, append_audit, current_ticket_id
from .boss_agent import boss_agent
from .config import get_usage_limits
from .mcp_toolset import get_plain_client

# Importing this package (triggered by the imports above) already wires up
# and registers all five agents with team.AGENT_REGISTRY, so Boss can
# delegate to any of the other four (full connectivity).

ROOT = Path(__file__).resolve().parent.parent
ORIGINAL_DB = ROOT / "data" / "campus_customs.db"
WORKING_DB = ROOT / "data" / "campus_customs_new.db"

app = FastAPI(title="Campus Customs Backend")

# The React dashboard (Vite dev server) runs on a different origin, so it
# needs CORS to call these routes from the browser.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ApprovePaymentRequest(BaseModel):
    kind: str
    ref_id: int
    amount: float
    account: str = "checking"
    approved_by: str


@app.get("/tickets")
async def list_tickets() -> dict[str, Any]:
    """Return the three tickets and whether each is open or resolved."""
    async with get_plain_client() as client:
        result = await client.call_tool("get_all_tickets", {})
    return result.data


@app.post("/tickets/{ticket_id}/run")
async def run_ticket(ticket_id: int) -> dict[str, Any]:
    """Run the agent team on one ticket, starting with Boss."""
    async with get_plain_client() as client:
        tickets_result = await client.call_tool("get_all_tickets", {})
    ticket = next(
        (t for t in tickets_result.data["tickets"] if t["id"] == ticket_id), None
    )
    if ticket is None:
        raise HTTPException(status_code=404, detail=f"Ticket {ticket_id} not found")

    token = current_ticket_id.set(ticket_id)
    try:
        task = (
            f"Resolve ticket {ticket['id']} ({ticket['type']}): {ticket['subject']}. "
            f"Requester: {ticket['requester']}. Notes: {ticket['notes']}. "
            f"sku={ticket['sku']} size={ticket['size']} qty={ticket['qty']} "
            f"lease_id={ticket['lease_id']} invoice_id={ticket['invoice_id']}."
        )
        result = await boss_agent.run(task, usage_limits=get_usage_limits())
    finally:
        current_ticket_id.reset(token)

    append_audit(
        agent="boss",
        step_type="final_output",
        detail={"ticket_id": ticket_id, "output": str(result.output)},
        ticket_id=ticket_id,
    )
    return {"ticket_id": ticket_id, "output": str(result.output)}


@app.get("/events")
async def recent_events(limit: int = 50) -> dict[str, Any]:
    """Return recent agent events — what each agent said and which tool it
    used — so the dashboard board can refresh."""
    if not AUDIT_PATH.exists():
        return {"events": []}
    trail = json.loads(AUDIT_PATH.read_text())
    return {"events": trail[-limit:]}


@app.post("/payments/approve")
async def approve_payment(req: ApprovePaymentRequest) -> dict[str, Any]:
    """The only route that actually moves cash. Agents can only prepare a
    payment recommendation; a human must call this after clicking Approve."""
    if not req.approved_by:
        raise HTTPException(status_code=400, detail="approved_by is required")

    async with get_plain_client() as client:
        result = await client.call_tool(
            "record_payment",
            {
                "kind": req.kind,
                "ref_id": req.ref_id,
                "amount": req.amount,
                "account": req.account,
                "approved_by": req.approved_by,
            },
        )

    append_audit(
        agent="human",
        step_type="tool_call",
        detail={"tool": "record_payment", "args": req.model_dump(), "result": result.data},
    )

    if not result.data.get("ok"):
        raise HTTPException(status_code=400, detail=result.data.get("reason"))
    return result.data


@app.get("/cash/balance")
async def cash_balance(account: str = "checking") -> dict[str, Any]:
    """Return the current balance for a cash account (default: checking)."""
    async with get_plain_client() as client:
        result = await client.call_tool("get_cash_balance", {"account": account})
    return result.data


@app.post("/reset")
async def reset_database() -> dict[str, Any]:
    """Reset the working database back to the original shop values, for a
    fresh run. The original data/campus_customs.db is never modified."""
    shutil.copyfile(ORIGINAL_DB, WORKING_DB)
    append_audit(agent="system", step_type="tool_call", detail={"tool": "reset_database"})
    return {"ok": True}
