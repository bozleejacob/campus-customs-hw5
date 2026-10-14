"""The single connection point to the shop's MCP server.

Every agent gets its shop facts (inventory, pricing, leases, vendors,
invoices, cash, tickets) through this toolset. Nothing in the backend talks
to data/campus_customs_new.db directly — that would be a second shop-tools
layer bypassing the MCP server, which we don't want.
"""

from __future__ import annotations

from pathlib import Path

from pydantic_ai.mcp import FastMCPClient, MCPToolset, StdioTransport

from .audit import append_audit

ROOT = Path(__file__).resolve().parent.parent
SERVER_PATH = ROOT / "mcp_server" / "server.py"
PYTHON_PATH = ROOT / ".venv" / "Scripts" / "python.exe"


def get_plain_client() -> FastMCPClient:
    """A bare MCP client for one-off reads/writes (dashboard polling, the
    payment-approval and reset routes) — no per-call audit wrapping, since
    those aren't agent-loop steps."""

    transport = StdioTransport(command=str(PYTHON_PATH), args=[str(SERVER_PATH)])
    return FastMCPClient(transport)


def get_shop_toolset(agent_name: str) -> MCPToolset:
    """One toolset per agent, so each agent's stdio session to the MCP server
    is independent, with every call to it logged to the audit trail."""

    transport = StdioTransport(command=str(PYTHON_PATH), args=[str(SERVER_PATH)])
    client = FastMCPClient(transport)

    async def process_tool_call(ctx, call_tool, tool_name, args):
        result = await call_tool(tool_name, args)
        append_audit(
            agent=agent_name,
            step_type="tool_call",
            detail={"tool": tool_name, "args": args, "result": result},
        )
        return result

    toolset = MCPToolset(client, process_tool_call=process_tool_call)

    # Agents can only prepare/recommend a payment in their output — the only
    # thing that actually moves cash is a human clicking Approve on the
    # dashboard (POST /payments/approve). So record_payment is withheld from
    # every agent's toolset, not just discouraged by prompt wording.
    return toolset.filtered(lambda ctx, tool_def: tool_def.name != "record_payment")
