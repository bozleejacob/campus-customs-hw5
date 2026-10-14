"""Shared data types for the Campus Customs agent team.

These mirror the shape of what the MCP tools return (and what they accept),
so agent code never has to guess the shape of a shop fact.
"""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel

AgentName = Literal["boss", "inventory", "accounting", "facilities", "customer_service"]


class Ticket(BaseModel):
    id: int
    type: str
    requester: str
    subject: str
    sku: Optional[str] = None
    size: Optional[str] = None
    qty: Optional[int] = None
    lease_id: Optional[int] = None
    invoice_id: Optional[int] = None
    status: str
    notes: Optional[str] = None
    created_at: str


class InventoryLevel(BaseModel):
    found: bool
    sku: Optional[str] = None
    name: Optional[str] = None
    size: Optional[str] = None
    qty: Optional[int] = None
    location: Optional[str] = None


class SkuPricing(BaseModel):
    found: bool
    sku: Optional[str] = None
    unit_cost: Optional[float] = None
    list_price: Optional[float] = None


class LeaseDetails(BaseModel):
    found: bool
    lease_id: Optional[int] = None
    space_name: Optional[str] = None
    landlord: Optional[str] = None
    monthly_rent: Optional[float] = None
    next_due: Optional[str] = None
    notes: Optional[str] = None


class VendorInfo(BaseModel):
    found: bool
    vendor_id: Optional[int] = None
    name: Optional[str] = None
    specialty: Optional[str] = None
    lead_days: Optional[int] = None


class InvoiceStatus(BaseModel):
    found: bool
    invoice_id: Optional[int] = None
    vendor_id: Optional[int] = None
    amount: Optional[float] = None
    due_date: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None


class CashBalance(BaseModel):
    found: bool
    account: Optional[str] = None
    balance: Optional[float] = None
    as_of: Optional[str] = None


class DeskToday(BaseModel):
    found: bool
    date_today: Optional[str] = None
    notes: Optional[str] = None


class PaymentResult(BaseModel):
    ok: bool
    reason: Optional[str] = None
    payment_id: Optional[int] = None
    new_balance: Optional[float] = None


class AuditRecord(BaseModel):
    timestamp: str
    agent: str  # one of AgentName, or "human" / "system" for API-triggered events
    ticket_id: Optional[int] = None
    step_type: Literal["tool_call", "delegation", "final_output"]
    detail: dict
