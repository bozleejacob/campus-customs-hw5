import { useCallback, useEffect, useState } from "react";
import "./App.css";
import {
  approvePayment,
  fetchCashBalance,
  fetchEvents,
  fetchTickets,
  resetDatabase,
  runTicket,
} from "./api";
import type { AgentEvent, ApprovePaymentRequest, CashBalance, Ticket } from "./types";
import { TicketBoard } from "./components/TicketBoard";
import { AgentFeed } from "./components/AgentFeed";
import { CashMeter } from "./components/CashMeter";
import { SummaryPanel } from "./components/SummaryPanel";
import { ApprovalModal } from "./components/ApprovalModal";

const RESOLVED_KEY = "campus-customs-resolved-tickets";

function loadResolved(): Set<number> {
  try {
    const raw = localStorage.getItem(RESOLVED_KEY);
    if (!raw) return new Set();
    return new Set(JSON.parse(raw) as number[]);
  } catch {
    return new Set();
  }
}

function saveResolved(ids: Set<number>) {
  localStorage.setItem(RESOLVED_KEY, JSON.stringify([...ids]));
}

export default function App() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [runningId, setRunningId] = useState<number | null>(null);
  const [events, setEvents] = useState<AgentEvent[]>([]);
  const [resolvedIds, setResolvedIds] = useState<Set<number>>(() => loadResolved());
  const [cash, setCash] = useState<CashBalance | null>(null);
  const [showApprove, setShowApprove] = useState(false);
  const [banner, setBanner] = useState<string | null>(null);

  const loadTickets = useCallback(async () => {
    const { tickets } = await fetchTickets();
    setTickets(tickets);
  }, []);

  const loadCash = useCallback(async () => {
    const c = await fetchCashBalance();
    setCash(c);
  }, []);

  const loadEvents = useCallback(async () => {
    const { events } = await fetchEvents();
    setEvents(events);
  }, []);

  useEffect(() => {
    loadTickets();
    loadCash();
    loadEvents();
  }, [loadTickets, loadCash, loadEvents]);

  // Poll cash + events continuously (cheap GETs), faster while a run is live.
  useEffect(() => {
    const interval = window.setInterval(
      () => {
        loadCash();
        loadEvents();
      },
      runningId !== null ? 1200 : 4000
    );
    return () => window.clearInterval(interval);
  }, [runningId, loadCash, loadEvents]);

  async function handleRun(id: number) {
    setRunningId(id);
    setSelectedId(id);
    setBanner(null);
    try {
      await runTicket(id);
      await Promise.all([loadEvents(), loadCash(), loadTickets()]);
      setResolvedIds((prev) => {
        const next = new Set(prev);
        next.add(id);
        saveResolved(next);
        return next;
      });
      setBanner(`✅ Ticket #${id} resolved by the team.`);
    } catch (err) {
      setBanner(`⚠ Run failed: ${err instanceof Error ? err.message : "unknown error"}`);
    } finally {
      setRunningId(null);
    }
  }

  async function handleApprove(req: ApprovePaymentRequest) {
    await approvePayment(req);
    await loadCash();
    setBanner("💵 Payment approved and recorded.");
  }

  async function handleReset() {
    await resetDatabase();
    setResolvedIds(new Set());
    saveResolved(new Set());
    setEvents([]);
    setSelectedId(null);
    setBanner("♻ Shop reset to original values. Fresh run ready.");
    await Promise.all([loadTickets(), loadCash()]);
  }

  const selectedTicket = tickets.find((t) => t.id === selectedId) ?? null;
  const ticketEvents = selectedId ? events.filter((e) => e.ticket_id === selectedId) : events;

  const approveDefaults: Partial<ApprovePaymentRequest> = selectedTicket
    ? {
        kind: selectedTicket.invoice_id ? "invoice" : selectedTicket.lease_id ? "lease" : "other",
        ref_id: selectedTicket.invoice_id ?? selectedTicket.lease_id ?? undefined,
        account: "checking",
      }
    : { account: "checking" };

  return (
    <div className="app">
      <header className="app__header">
        <div>
          <h1>🐶 Campus Customs — Agent Desk</h1>
          <p>Boss, Inventory, Accounting, Facilities &amp; Customer Service, live.</p>
        </div>
        <div className="app__header-actions">
          <CashMeter balance={cash?.balance ?? null} asOf={cash?.as_of ?? null} />
          <button className="btn btn--ghost" onClick={() => setShowApprove(true)}>
            💵 Approve Payment
          </button>
          <button className="btn btn--danger" onClick={handleReset}>
            ♻ Reset Shop
          </button>
        </div>
      </header>

      {banner && <div className="banner">{banner}</div>}

      <main className="app__main">
        <section className="app__board">
          <h2>Tickets</h2>
          <TicketBoard
            tickets={tickets}
            selectedId={selectedId}
            runningId={runningId}
            resolvedIds={resolvedIds}
            onSelect={setSelectedId}
            onRun={handleRun}
          />
        </section>

        <section className="app__feed">
          <AgentFeed events={ticketEvents} running={runningId !== null} />
          {selectedId && <SummaryPanel ticketId={selectedId} events={events} />}
        </section>
      </main>

      {showApprove && (
        <ApprovalModal
          defaults={approveDefaults}
          onClose={() => setShowApprove(false)}
          onApprove={handleApprove}
        />
      )}
    </div>
  );
}
