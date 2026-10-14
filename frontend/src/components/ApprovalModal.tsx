import { useState } from "react";
import type { ApprovePaymentRequest } from "../types";

interface Props {
  defaults: Partial<ApprovePaymentRequest>;
  onClose: () => void;
  onApprove: (req: ApprovePaymentRequest) => Promise<void>;
}

export function ApprovalModal({ defaults, onClose, onApprove }: Props) {
  const [kind, setKind] = useState(defaults.kind ?? "invoice");
  const [refId, setRefId] = useState(String(defaults.ref_id ?? ""));
  const [amount, setAmount] = useState(String(defaults.amount ?? ""));
  const [account, setAccount] = useState(defaults.account ?? "checking");
  const [approvedBy, setApprovedBy] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setBusy(true);
    try {
      await onApprove({
        kind,
        ref_id: Number(refId),
        amount: Number(amount),
        account,
        approved_by: approvedBy,
      });
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Payment was refused.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <form
        className="modal"
        onClick={(e) => e.stopPropagation()}
        onSubmit={handleSubmit}
      >
        <h2>✅ Approve a Payment</h2>
        <p className="modal__sub">
          Read what the agents recommended, then approve it here. This is the
          only thing that actually moves cash.
        </p>

        <label>
          Kind
          <select value={kind} onChange={(e) => setKind(e.target.value)}>
            <option value="invoice">invoice</option>
            <option value="lease">lease</option>
            <option value="other">other</option>
          </select>
        </label>

        <label>
          Reference ID
          <input
            type="number"
            value={refId}
            onChange={(e) => setRefId(e.target.value)}
            required
          />
        </label>

        <label>
          Amount (USD)
          <input
            type="number"
            step="0.01"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            required
          />
        </label>

        <label>
          Account
          <input value={account} onChange={(e) => setAccount(e.target.value)} />
        </label>

        <label>
          Your name (approver)
          <input
            value={approvedBy}
            onChange={(e) => setApprovedBy(e.target.value)}
            placeholder="required to approve"
            required
          />
        </label>

        {error && <div className="modal__error">⚠ {error}</div>}

        <div className="modal__actions">
          <button type="button" className="btn btn--ghost" onClick={onClose}>
            Cancel
          </button>
          <button type="submit" className="btn btn--primary" disabled={busy}>
            {busy ? "Approving…" : "Approve payment"}
          </button>
        </div>
      </form>
    </div>
  );
}
