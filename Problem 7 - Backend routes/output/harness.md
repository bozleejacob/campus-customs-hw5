# Backend Routes — Problem 7

Server: `backend/main.py` (FastAPI), started from `backend/` with `uvicorn main:app --reload --port 8000`, serving at `http://localhost:8000`.

- **GET /tickets** — returns all three tickets, each with its current status (open/resolved).
- **POST /tickets/{ticket_id}/run** — runs the agent team (starting with Boss) on that ticket and returns its final output.
- **GET /events** — returns recent agent-loop events (agent, tool used, output) from the audit trail, so the board can refresh.
- **POST /payments/approve** — the only route that actually moves cash; calls `record_payment` after a human clicks Approve and supplies `approved_by`.
- **GET /cash/balance** — returns the current balance (default account: `checking`) from `cash_accounts`.
- **POST /reset** — resets the working database back to the shop's original values for a fresh run.
