"""FastMCP server for the Campus Customs shop database."""

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from fastmcp import FastMCP

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "campus_customs_new.db"

mcp = FastMCP("campus-customs")


def _connect() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)


@mcp.tool()
def get_inventory_level(sku: str, size: str) -> dict:
    """Look up on-hand quantity and location for a SKU/size in the inventory table."""
    conn = _connect()
    cur = conn.cursor()
    cur.execute(
        "SELECT sku, name, size, qty, location FROM inventory WHERE sku = ? AND size = ?",
        (sku, size),
    )
    row = cur.fetchone()
    conn.close()
    if row is None:
        return {"found": False, "sku": sku, "size": size}
    return {
        "found": True,
        "sku": row[0],
        "name": row[1],
        "size": row[2],
        "qty": row[3],
        "location": row[4],
    }


@mcp.tool()
def get_sku_pricing(sku: str) -> dict:
    """Look up unit cost and list price for a SKU in the pricing table."""
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT sku, unit_cost, list_price FROM pricing WHERE sku = ?", (sku,))
    row = cur.fetchone()
    conn.close()
    if row is None:
        return {"found": False, "sku": sku}
    return {"found": True, "sku": row[0], "unit_cost": row[1], "list_price": row[2]}


@mcp.tool()
def get_open_tickets() -> dict:
    """List every ticket in the tickets table whose status is 'open'."""
    conn = _connect()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, type, requester, subject, sku, size, qty, lease_id, invoice_id, "
        "status, notes, created_at FROM tickets WHERE status = 'open' ORDER BY id"
    )
    rows = cur.fetchall()
    conn.close()
    cols = [
        "id", "type", "requester", "subject", "sku", "size", "qty",
        "lease_id", "invoice_id", "status", "notes", "created_at",
    ]
    return {"tickets": [dict(zip(cols, row)) for row in rows]}


@mcp.tool()
def get_all_tickets() -> dict:
    """List every ticket in the tickets table, regardless of status, so a
    dashboard can show which are open and which are resolved."""
    conn = _connect()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, type, requester, subject, sku, size, qty, lease_id, invoice_id, "
        "status, notes, created_at FROM tickets ORDER BY id"
    )
    rows = cur.fetchall()
    conn.close()
    cols = [
        "id", "type", "requester", "subject", "sku", "size", "qty",
        "lease_id", "invoice_id", "status", "notes", "created_at",
    ]
    return {"tickets": [dict(zip(cols, row)) for row in rows]}


@mcp.tool()
def get_desk_today() -> dict:
    """Read the shop's 'today' date and desk notes from the desk table."""
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT date_today, notes FROM desk LIMIT 1")
    row = cur.fetchone()
    conn.close()
    if row is None:
        return {"found": False}
    return {"found": True, "date_today": row[0], "notes": row[1]}


@mcp.tool()
def get_cash_balance(account: str = "checking") -> dict:
    """Look up the current balance and as-of date for a cash account."""
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT name, balance, date FROM cash_accounts WHERE name = ?", (account,))
    row = cur.fetchone()
    conn.close()
    if row is None:
        return {"found": False, "account": account}
    return {"found": True, "account": row[0], "balance": row[1], "as_of": row[2]}


@mcp.tool()
def get_vendor(vendor_id: int) -> dict:
    """Look up a vendor's name, specialty, and restock lead time in the vendors table."""
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT id, name, specialty, lead_days FROM vendors WHERE id = ?", (vendor_id,))
    row = cur.fetchone()
    conn.close()
    if row is None:
        return {"found": False, "vendor_id": vendor_id}
    return {
        "found": True,
        "vendor_id": row[0],
        "name": row[1],
        "specialty": row[2],
        "lead_days": row[3],
    }


@mcp.tool()
def get_invoice(invoice_id: int) -> dict:
    """Look up a vendor invoice's amount, due date, and status in the invoices table."""
    conn = _connect()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, vendor_id, amount, due_date, status, description FROM invoices WHERE id = ?",
        (invoice_id,),
    )
    row = cur.fetchone()
    conn.close()
    if row is None:
        return {"found": False, "invoice_id": invoice_id}
    return {
        "found": True,
        "invoice_id": row[0],
        "vendor_id": row[1],
        "amount": row[2],
        "due_date": row[3],
        "status": row[4],
        "description": row[5],
    }


@mcp.tool()
def record_payment(kind: str, ref_id: int, amount: float, account: str, approved_by: str) -> dict:
    """Pay an invoice or lease from a cash account. Requires a human approver name
    (approved_by) and refuses if the account balance would go negative. On success,
    writes a row to payments, debits cash_accounts, and marks the matching invoice
    'paid' (kind='invoice')."""
    if not approved_by:
        return {"ok": False, "reason": "human approval (approved_by) is required for any payment"}
    if amount <= 0:
        return {"ok": False, "reason": "amount must be positive"}

    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT balance FROM cash_accounts WHERE name = ?", (account,))
    row = cur.fetchone()
    if row is None:
        conn.close()
        return {"ok": False, "reason": f"unknown account '{account}'"}

    balance = row[0]
    if balance - amount < 0:
        conn.close()
        return {"ok": False, "reason": "insufficient funds: payment would make balance negative"}

    new_balance = balance - amount
    paid_at = datetime.now(timezone.utc).isoformat()

    cur.execute(
        "INSERT INTO payments (kind, ref_id, amount, account, paid_at, approved_by) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (kind, ref_id, amount, account, paid_at, approved_by),
    )
    payment_id = cur.lastrowid
    cur.execute("UPDATE cash_accounts SET balance = ?, date = ? WHERE name = ?", (new_balance, paid_at[:10], account))
    if kind == "invoice":
        cur.execute("UPDATE invoices SET status = 'paid' WHERE id = ?", (ref_id,))
    conn.commit()
    conn.close()
    return {"ok": True, "payment_id": payment_id, "new_balance": new_balance}


@mcp.tool()
def get_lease_details(lease_id: int) -> dict:
    """Look up rent, due date, and landlord for a lease in the leases table."""
    conn = _connect()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, space_name, landlord, monthly_rent, next_due, notes FROM leases WHERE id = ?",
        (lease_id,),
    )
    row = cur.fetchone()
    conn.close()
    if row is None:
        return {"found": False, "lease_id": lease_id}
    return {
        "found": True,
        "lease_id": row[0],
        "space_name": row[1],
        "landlord": row[2],
        "monthly_rent": row[3],
        "next_due": row[4],
        "notes": row[5],
    }


if __name__ == "__main__":
    mcp.run()
