# Database Harness — Campus Customs

Working copy: `data/campus_customs_new.db` (copied from `data/campus_customs.db`, the original stays untouched for resets).

## Tables

- **desk** — `date_today`, `notes` — Gives the agents "today," which decides what's overdue on invoices, leases, and tickets.
- **tickets** — `id`, `type`, `requester`, `subject`, `sku`, `size`, `qty`, `lease_id`, `invoice_id`, `status`, `notes`, `created_at` — The work queue; every agent reads this to know what's open and who asked for what.
- **inventory** — `sku`, `name`, `size`, `qty`, `location` — Tells Inventory what's in stock by SKU/size so it can spot shortfalls and restock needs.
- **pricing** — `sku`, `unit_cost`, `list_price` — Lets Accounting/Inventory compute margins and value restocks correctly.
- **vendors** — `id`, `name`, `specialty`, `lead_days` — Tells Inventory who can restock a SKU and how long it'll take.
- **leases** — `id`, `space_name`, `landlord`, `monthly_rent`, `next_due`, `notes` — Facilities uses this for rent and lease-space obligations.
- **cash_accounts** — `name`, `balance`, `date` — Accounting checks this before approving any payment so the shop never goes negative.
- **payments** — `id`, `kind`, `ref_id`, `amount`, `account`, `paid_at`, `approved_by` — The record of money actually paid out, written only after human approval.
- **invoices** — `id`, `vendor_id`, `amount`, `due_date`, `status`, `description` — Accounting watches this for unpaid vendor bills, which also blocks new restock shipments.
