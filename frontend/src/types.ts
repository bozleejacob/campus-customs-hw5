export interface Ticket {
  id: number;
  type: string;
  requester: string;
  subject: string;
  sku: string | null;
  size: string | null;
  qty: number | null;
  lease_id: number | null;
  invoice_id: number | null;
  status: string;
  notes: string | null;
  created_at: string;
}

export type StepType = "tool_call" | "delegation" | "final_output";

export interface AgentEvent {
  timestamp: string;
  agent: string;
  ticket_id: number | null;
  step_type: StepType;
  detail: Record<string, unknown>;
}

export interface CashBalance {
  found: boolean;
  account: string;
  balance: number;
  as_of: string;
}

export interface RunResult {
  ticket_id: number;
  output: string;
}

export interface ApprovePaymentRequest {
  kind: string;
  ref_id: number;
  amount: number;
  account: string;
  approved_by: string;
}

export interface ApprovePaymentResult {
  ok: boolean;
  reason?: string;
  payment_id?: number;
  new_balance?: number;
}

export const AGENT_NAMES = [
  "boss",
  "inventory",
  "accounting",
  "facilities",
  "customer_service",
] as const;

export type AgentName = (typeof AGENT_NAMES)[number] | "human" | "system";
