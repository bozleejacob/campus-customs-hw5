# Agent Team Harness — Problem 5

Five PydanticAI agents (`backend/boss_agent.py`, `inventory_agent.py`, `accounting_agent.py`, `facilities_agent.py`, `customer_service_agent.py`), each running `gpt-5.6-luna` through Portkey (`PORTKEY_API_KEY`, `base_url=https://api.portkey.ai/v1`). Every agent has full connectivity — a `delegate(to_agent, task)` tool that can reach any of the other four (`backend/team.py`). All shop facts come from the MCP server (`mcp_server/server.py`) over `data/campus_customs_new.db` — no agent talks to the database directly.

## Agents and their MCP tools

- **Boss** (`backend/prompts/boss.md`) — reads every open ticket and makes the final call.
  - `get_open_tickets()` → `tickets`
- **Inventory** (`backend/prompts/inventory.md`) — checks stock, spots shortfalls, finds restock vendors.
  - `get_inventory_level(sku, size)` → `inventory`
  - `get_vendor(vendor_id)` → `vendors`
  - `get_invoice(invoice_id)` → `invoices`
- **Accounting** (`backend/prompts/accounting.md`) — watches cash and invoices, checks margins, prepares payments for human approval.
  - `get_cash_balance(account)` → `cash_accounts`
  - `get_invoice(invoice_id)` → `invoices`
  - `get_sku_pricing(sku)` → `pricing`
  - Does **not** have `record_payment` — see below, it's withheld from every agent.
- **Facilities** (`backend/prompts/facilities.md`) — handles leases, rent, and shop-space notices.
  - `get_lease_details(lease_id)` → `leases`
  - `get_desk_today()` → `desk`
- **Customer Service** (`backend/prompts/customer_service.md`) — drafts customer messages, never sends them.
  - No dedicated shop-fact tool of its own; it delegates to Boss/Inventory/Accounting for any fact it needs before drafting.

All five agents also share `get_desk_today()` indirectly through delegation, since "today" matters to every overdue judgment call.

## Safety guardrails (real customers, real money)

- **No real outreach.** Customer Service only drafts messages; nothing in the backend emails a customer or calls a vendor. Drafts stay on the board for a human to send.
- **Human-in-the-loop payments.** `record_payment` is withheld from every agent's MCP toolset entirely (`backend/mcp_toolset.py` filters it out) — agents can only recommend a payment in their output. Only the FastAPI backend's `/payments/approve` route, called after a human clicks Approve, can invoke `record_payment`, and it still requires an `approved_by` name.
- **No negative balances.** `record_payment` checks the account balance first and refuses if the payment would take it below zero.
- **Vendor shipping rule enforced by data, not trust.** Agents check `get_invoice` before promising a restock, since a vendor with an open unpaid invoice won't ship.
- **Single source of truth.** All shop facts come from the MCP server over the working copy of the database; agents are instructed to never invent a quantity, price, balance, or date.
- **Reset safety.** The original `data/campus_customs.db` is never touched — only `data/campus_customs_new.db` is written to, so the shop can always be reset for a fresh run.

## Token-usage guardrails

- **Per-call output cap.** Every agent's `model_settings` caps `max_tokens` at 600 per model response (`backend/config.py`).
- **Per-run step cap.** `UsageLimits(request_limit=8)` caps each agent run at 8 tool calls/model requests.
- **Per-run token cap.** `UsageLimits(total_tokens_limit=4000)` caps each agent run at 4,000 total tokens.
- **Shared budget across delegation.** When one agent delegates to another, the child run is passed the parent's `usage` object, so the 4,000-token cap applies to the whole delegation chain for a ticket, not a fresh 4,000 per hop.
- **Delegation depth cap.** `MAX_DELEGATION_DEPTH = 2` stops a task from being bounced agent-to-agent indefinitely; a `delegate` call beyond that depth is refused and logged.

## Audit trail

Every tool call, delegation, and delegated final output appends a record (timestamp, agent, ticket_id, step type, detail) to `Problem 5 - Build the agent team and grow the MCP tools/output/audit_trail.json` (`backend/audit.py`). The file is read-appended-rewritten each time, never wiped at the start of a run, so history survives across runs.
