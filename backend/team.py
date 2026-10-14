"""Full-connectivity delegation: every agent can hand a task to every other
agent. Guardrails here (delegation depth, shared usage budget) keep a
multi-agent handoff from running away on tokens or tool calls.
"""

from __future__ import annotations

import contextvars
from typing import TYPE_CHECKING, Any, Awaitable, Callable, Dict

from pydantic_ai import RunContext

from .audit import append_audit
from .config import MAX_DELEGATION_DEPTH, get_usage_limits
from .models import AgentName

if TYPE_CHECKING:
    from pydantic_ai import Agent

AGENT_REGISTRY: Dict[str, "Agent"] = {}

_delegation_depth: contextvars.ContextVar[int] = contextvars.ContextVar(
    "delegation_depth", default=0
)


def register_agent(name: AgentName, agent: "Agent") -> None:
    AGENT_REGISTRY[name] = agent


def make_delegate_tool(
    caller: AgentName,
) -> Callable[[RunContext, AgentName, str], Awaitable[str]]:
    """Builds the `delegate` tool for one agent, with the caller's name
    captured by closure so every audit entry shows who handed off to whom."""

    async def delegate(ctx: RunContext[Any], to_agent: AgentName, task: str) -> str:
        """Hand a task to another Campus Customs agent (boss, inventory,
        accounting, facilities, or customer_service) and return its answer."""
        depth = _delegation_depth.get()

        if depth >= MAX_DELEGATION_DEPTH:
            append_audit(
                agent=caller,
                step_type="delegation",
                detail={
                    "to": to_agent,
                    "task": task,
                    "blocked": f"max delegation depth ({MAX_DELEGATION_DEPTH}) reached",
                },
            )
            return f"Delegation blocked: max depth reached, {to_agent} was not called."

        target = AGENT_REGISTRY.get(to_agent)
        if target is None:
            return f"Unknown agent '{to_agent}'."

        append_audit(agent=caller, step_type="delegation", detail={"to": to_agent, "task": task})

        token = _delegation_depth.set(depth + 1)
        try:
            result = await target.run(
                task,
                usage=ctx.usage,
                usage_limits=ctx.usage_limits or get_usage_limits(),
            )
        finally:
            _delegation_depth.reset(token)

        append_audit(
            agent=to_agent,
            step_type="final_output",
            detail={"delegated_from": caller, "task": task, "output": str(result.output)},
        )
        return str(result.output)

    return delegate
