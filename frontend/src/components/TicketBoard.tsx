import type { Ticket } from "../types";

interface Props {
  tickets: Ticket[];
  selectedId: number | null;
  runningId: number | null;
  resolvedIds: Set<number>;
  onSelect: (id: number) => void;
  onRun: (id: number) => void;
}

const TYPE_LABEL: Record<string, string> = {
  customer_order: "Customer Order",
  rent_notice: "Rent Notice",
  price_override: "Price Override",
};

export function TicketBoard({
  tickets,
  selectedId,
  runningId,
  resolvedIds,
  onSelect,
  onRun,
}: Props) {
  return (
    <div className="ticket-board">
      {tickets.map((t) => {
        const resolved = resolvedIds.has(t.id);
        const running = runningId === t.id;
        const selected = selectedId === t.id;
        return (
          <button
            key={t.id}
            className={[
              "ticket-card",
              selected ? "ticket-card--selected" : "",
              resolved ? "ticket-card--resolved" : "",
              running ? "ticket-card--running" : "",
            ].join(" ")}
            onClick={() => onSelect(t.id)}
          >
            <div className="ticket-card__pin" />
            <div className="ticket-card__head">
              <span className="ticket-card__id">#{t.id}</span>
              <span className="ticket-card__type">
                {TYPE_LABEL[t.type] ?? t.type}
              </span>
            </div>
            <h3 className="ticket-card__subject">{t.subject}</h3>
            <p className="ticket-card__requester">from {t.requester}</p>
            {t.notes && <p className="ticket-card__notes">"{t.notes}"</p>}

            <div className="ticket-card__footer">
              <span
                className={[
                  "status-pill",
                  resolved ? "status-pill--resolved" : "status-pill--open",
                ].join(" ")}
              >
                {resolved ? "✓ resolved" : "open"}
              </span>

              <span
                role="button"
                tabIndex={0}
                className="run-btn"
                onClick={(e) => {
                  e.stopPropagation();
                  if (!running) onRun(t.id);
                }}
              >
                {running ? (
                  <>
                    <span className="live-dot" /> running…
                  </>
                ) : (
                  "▶ run team"
                )}
              </span>
            </div>
          </button>
        );
      })}
    </div>
  );
}
