import { useEffect, useRef } from "react";
import type { AgentEvent } from "../types";
import { metaFor } from "../agentMeta";
import { textOf, unwrapDetail } from "../eventDetail";

interface Props {
  events: AgentEvent[];
  running: boolean;
}

function describe(event: AgentEvent): string {
  const d = unwrapDetail(event.detail as Record<string, unknown>);
  switch (event.step_type) {
    case "tool_call": {
      const tool = String(d.tool ?? "a tool");
      const args = d.args ? JSON.stringify(d.args) : "{}";
      return `called ${tool}(${args})`;
    }
    case "delegation": {
      const to = String(d.to ?? "someone");
      if (d.blocked) {
        return `tried to hand off to ${to} — blocked (${d.blocked})`;
      }
      return `handed this off to ${to}: "${String(d.task ?? "")}"`;
    }
    case "final_output":
    default: {
      return `said: "${textOf(d, "output")}"`;
    }
  }
}

export function AgentFeed({ events, running }: Props) {
  const bottomRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [events.length]);

  return (
    <div className="agent-feed">
      <div className="agent-feed__header">
        <span>Agent Chatter</span>
        {running && (
          <span className="agent-feed__live">
            <span className="live-dot" /> live
          </span>
        )}
      </div>
      <div className="agent-feed__body">
        {events.length === 0 && (
          <p className="agent-feed__empty">
            Nothing yet — pick a ticket and run the team to hear them talk it out.
          </p>
        )}
        {events.map((e, i) => {
          const meta = metaFor(e.agent);
          return (
            <div
              className="feed-line"
              key={i}
              style={{ animationDelay: `${Math.min(i, 20) * 25}ms` }}
            >
              <span
                className="feed-line__avatar"
                style={{ background: meta.color + "33", borderColor: meta.color }}
              >
                {meta.emoji}
              </span>
              <div className="feed-line__body">
                <div className="feed-line__meta">
                  <span className="feed-line__agent" style={{ color: meta.color }}>
                    {meta.label}
                  </span>
                  <span className="feed-line__step">{e.step_type.replace("_", " ")}</span>
                  <span className="feed-line__time">
                    {new Date(e.timestamp).toLocaleTimeString()}
                  </span>
                </div>
                <div className="feed-line__text">{describe(e)}</div>
              </div>
            </div>
          );
        })}
        <div ref={bottomRef} />
      </div>
    </div>
  );
}
