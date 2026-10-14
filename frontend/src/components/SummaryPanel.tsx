import type { AgentEvent } from "../types";
import { metaFor } from "../agentMeta";
import { textOf, unwrapDetail } from "../eventDetail";

interface Props {
  ticketId: number;
  events: AgentEvent[];
}

interface AgentSummary {
  agent: string;
  tools: string[];
  lastSaid: string | null;
}

function summarize(ticketId: number, events: AgentEvent[]): AgentSummary[] {
  const byAgent = new Map<string, AgentSummary>();

  for (const e of events) {
    if (e.ticket_id !== ticketId) continue;
    const entry =
      byAgent.get(e.agent) ?? { agent: e.agent, tools: [], lastSaid: null };

    const d = unwrapDetail(e.detail as Record<string, unknown>);

    if (e.step_type === "tool_call") {
      const tool = String(d.tool ?? "");
      if (tool && !entry.tools.includes(tool)) entry.tools.push(tool);
    }
    if (e.step_type === "final_output") {
      entry.lastSaid = textOf(d, "output");
    }

    byAgent.set(e.agent, entry);
  }

  return [...byAgent.values()];
}

export function SummaryPanel({ ticketId, events }: Props) {
  const summaries = summarize(ticketId, events);

  if (summaries.length === 0) return null;

  return (
    <div className="summary-panel">
      <h2>What each agent did on ticket #{ticketId}</h2>
      <div className="summary-panel__grid">
        {summaries.map((s) => {
          const meta = metaFor(s.agent);
          return (
            <div className="summary-card" key={s.agent}>
              <div className="summary-card__head" style={{ borderColor: meta.color }}>
                <span>{meta.emoji}</span>
                <span style={{ color: meta.color }}>{meta.label}</span>
              </div>
              <div className="summary-card__tools">
                {s.tools.length > 0
                  ? s.tools.map((t) => (
                      <span className="tool-chip" key={t}>
                        {t}
                      </span>
                    ))
                  : "no tools called"}
              </div>
              {s.lastSaid && (
                <p className="summary-card__said">"{s.lastSaid}"</p>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
