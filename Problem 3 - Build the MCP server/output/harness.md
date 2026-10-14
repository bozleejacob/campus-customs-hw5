# MCP Tool Harness — Problem 3

Three tools in `mcp_server/server.py`, each reading one table and unlocking one open ticket.

- **get_inventory_level(sku, size)** — reads `inventory` — unlocks ticket **101** (customer_order, Tauhid Zaman, CC-TEE-WHITE size S, qty 1) — this is the right tool because inventory shows CC-TEE-WHITE size S at 0 units on hand, so it proves the order can't ship from stock and needs a restock decision.
- **get_sku_pricing(sku)** — reads `pricing` — unlocks ticket **103** (price_override, Yale AI Club, CC-HOOD-NAVY size M, qty 20 bulk discount) — this is the right tool because it gives unit_cost ($22) and list_price ($58) for CC-HOOD-NAVY, which is exactly what's needed to judge whether a bulk discount still clears a healthy margin.
- **get_lease_details(lease_id)** — reads `leases` — unlocks ticket **102** (rent_notice, Elm City Properties, lease_id 1) — this is the right tool because it returns the lease's next_due date (2026-09-02) and monthly rent, which is exactly what Facilities needs to judge how urgent the rent notice is against desk.date_today.
