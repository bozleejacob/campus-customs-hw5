# Campus Customs — Full System Harness

The complete agentic shop-ops system, end to end: database → MCP server → agent team → FastAPI backend → React dashboard. This consolidates what each earlier problem built; per-problem detail lives in each `Problem N .../output/harness.md`.

## 1. Database tables (`data/campus_customs_new.db`)

Working copy of `data/campus_customs.db`, which is never written to (reset always restores from it).

- **desk** — `date_today`, `notes` — the shop's authoritative "today," used to judge what's overdue.
- **tickets** — the work queue every agent reads to know what's open. Note: there is no MCP tool that writes `tickets.status`, so the raw DB column stays `open` even after a ticket is resolved — "resolved" is tracked via the agent's final output, the audit trail, and the dashboard's own resolved-state, not a status flip in this table.
- **inventory** — on-hand quantity/location by SKU + size.
- **pricing** — `unit_cost` / `list_price` per SKU, for margin and discount judgment.
- **vendors** — who can restock a SKU and their lead time.
- **leases** — rent, due dates, landlord per lease.
- **cash_accounts** — the shop's cash balance (only `checking` in this run).
- **payments** — the ledger of money actually paid out, written only by `record_payment`.
- **invoices** — vendor bills; an open one blocks that vendor from shipping.

## 2. MCP server tools (`mcp_server/server.py`, FastMCP)

| Tool | Table(s) | Purpose |
|---|---|---|
| `get_inventory_level(sku, size)` | inventory | on-hand qty + location |
| `get_sku_pricing(sku)` | pricing | unit cost / list price |
| `get_lease_details(lease_id)` | leases | rent, due date, landlord |
| `get_open_tickets()` | tickets | every open ticket |
| `get_all_tickets()` | tickets | every ticket, any status |
| `get_desk_today()` | desk | the shop's "today" |
| `get_cash_balance(account)` | cash_accounts | current balance |
| `get_vendor(vendor_id)` | vendors | name, specialty, lead time |
| `get_invoice(invoice_id)` | invoices | amount, due date, status |
| `record_payment(kind, ref_id, amount, account, approved_by)` | payments, cash_accounts, invoices | the only write tool — requires a human approver, refuses a negative balance |

## 3. The five agents (`backend/*_agent.py`, PydanticAI, `gpt-5.6-luna` via Portkey)

- **Boss** — reads open tickets, decides who works each one, makes the final call.
- **Inventory** — stock levels, shortfalls, restock vendors.
- **Accounting** — cash, invoices, margins; recommends payments (cannot call `record_payment` — that tool is filtered out of every agent's toolset).
- **Facilities** — leases, rent, due dates.
- **Customer Service** — drafts customer messages; never sends them.

All five share a `delegate(to_agent, task)` tool (`backend/team.py`) for full connectivity, under guardrails: max delegation depth 2, shared usage budget across a delegation chain (24 tool calls / 20,000 tokens per ticket run, 600 output tokens per model call). Every tool call, delegation, and final output appends to `Problem 5 .../output/audit_trail.json`, which is never wiped — it now holds the real transcripts from this run alongside earlier test entries.

## 4. API routes (`backend/main.py`, FastAPI, `http://localhost:8000`)

- `GET /tickets` — all tickets + status.
- `POST /tickets/{id}/run` — runs the agent team on one ticket.
- `GET /events` — recent audit-trail entries for the dashboard feed.
- `POST /payments/approve` — the only route that calls `record_payment`; requires `approved_by`.
- `GET /cash/balance` — current balance.
- `POST /reset` — restores the working database from the original.

CORS allows `http://localhost:5173` (the Vite dev server) so the browser can call these directly.

## 5. The dashboard (`frontend/`, React + Vite + TypeScript, `npm run dev`)

A corkboard of ticket cards you can select and run; a live "Agent Chatter" feed (polling `/events`) showing each agent's tool calls, delegations, and final answers as they happen; a per-agent summary once a ticket resolves; an Approve Payment modal that is the only path to moving cash; and a reactive cash meter that flashes when a payment clears. See `Problem 8 .../output/design.md` for the design reasoning.

## 6. Safety rules, and how this run respected them

- **No real outreach.** Customer Service drafted replies for tickets 101 and 103; neither was sent — they're left on the board for a human.
- **Human-in-the-loop payments.** Both real payments this run (invoice 501, lease 1 rent) were recommended by the agents and then approved explicitly by a human (`approved_by: "Jake"`) through `/payments/approve` — no agent called `record_payment`.
- **No negative balances.** Checked: $3,400.00 → $2,560.00 → $160.00, never below zero. `record_payment` would have refused otherwise.
- **Vendor shipping rule.** Ticket 101's resolution explicitly hinged on invoice 501 being open and blocking the vendor; paying it was the unblock.
- **Single source of truth.** Every fact in every agent's output traces back to an MCP tool call recorded in the audit trail — nothing was invented.
- **Reset safety.** The working database was reset from the untouched original before this run, and the original remains byte-for-byte unmodified.
