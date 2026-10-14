# MCP Server — Campus Customs

This is the MCP server (built with FastMCP) that all Campus Customs agents (Boss, Inventory, Accounting, Facilities, Customer Service) use to read and update the shop's data. It talks to the working copy of the database, `data/campus_customs_new.db` — never the original `data/campus_customs.db`, which stays untouched so the shop can be reset.

## Tools

- **get_inventory_level(sku, size)** — reads the `inventory` table. Returns on-hand quantity and location for a SKU/size.
- **get_sku_pricing(sku)** — reads the `pricing` table. Returns unit cost and list price for a SKU.
- **get_lease_details(lease_id)** — reads the `leases` table. Returns rent, next due date, and landlord for a lease.
- **get_open_tickets()** — reads the `tickets` table. Returns every ticket with status `open`.
- **get_desk_today()** — reads the `desk` table. Returns the shop's "today" date and desk notes.
- **get_cash_balance(account)** — reads the `cash_accounts` table. Returns the balance and as-of date for an account.
- **get_vendor(vendor_id)** — reads the `vendors` table. Returns a vendor's name, specialty, and restock lead time.
- **get_invoice(invoice_id)** — reads the `invoices` table. Returns a vendor invoice's amount, due date, and status.
- **record_payment(kind, ref_id, amount, account, approved_by)** — the only write tool. Requires a human approver name, refuses if the account balance would go negative, and on success writes a `payments` row, debits `cash_accounts`, and marks the matching invoice `paid`.

More tools will be added as later problems require them.
