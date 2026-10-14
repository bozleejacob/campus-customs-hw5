export interface AgentMeta {
  label: string;
  emoji: string;
  color: string;
}

export const AGENT_META: Record<string, AgentMeta> = {
  boss: { label: "Boss", emoji: "🧑‍💼", color: "#f2b705" },
  inventory: { label: "Inventory", emoji: "📦", color: "#3ba7ff" },
  accounting: { label: "Accounting", emoji: "💰", color: "#38d996" },
  facilities: { label: "Facilities", emoji: "🏢", color: "#c783ff" },
  customer_service: { label: "Customer Service", emoji: "💬", color: "#ff8a5c" },
  human: { label: "Human (you)", emoji: "🖐️", color: "#ffffff" },
  system: { label: "System", emoji: "🛠️", color: "#9aa4b8" },
};

export function metaFor(agent: string): AgentMeta {
  return (
    AGENT_META[agent] ?? { label: agent, emoji: "🐾", color: "#9aa4b8" }
  );
}
