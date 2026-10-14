import type {
  AgentEvent,
  ApprovePaymentRequest,
  ApprovePaymentResult,
  CashBalance,
  RunResult,
  Ticket,
} from "./types";

const BASE_URL = "http://localhost:8000";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  const body = await res.json();
  if (!res.ok) {
    const detail = typeof body?.detail === "string" ? body.detail : res.statusText;
    throw new Error(detail);
  }
  return body as T;
}

export function fetchTickets(): Promise<{ tickets: Ticket[] }> {
  return request("/tickets");
}

export function runTicket(ticketId: number): Promise<RunResult> {
  return request(`/tickets/${ticketId}/run`, { method: "POST" });
}

export function fetchEvents(limit = 200): Promise<{ events: AgentEvent[] }> {
  return request(`/events?limit=${limit}`);
}

export function approvePayment(
  payload: ApprovePaymentRequest
): Promise<ApprovePaymentResult> {
  return request("/payments/approve", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function fetchCashBalance(account = "checking"): Promise<CashBalance> {
  return request(`/cash/balance?account=${account}`);
}

export function resetDatabase(): Promise<{ ok: boolean }> {
  return request("/reset", { method: "POST" });
}
