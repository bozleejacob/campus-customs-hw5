"""Connects to mcp_server/server.py as a real MCP client (stdio) and calls each tool once."""

import asyncio
import datetime
import json
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = Path(__file__).resolve().parent / "output" / "mcp_smoke.json"

CALLS = [
    {"ticket": 101, "tool": "get_inventory_level", "args": {"sku": "CC-TEE-WHITE", "size": "S"}},
    {"ticket": 103, "tool": "get_sku_pricing", "args": {"sku": "CC-HOOD-NAVY"}},
    {"ticket": 102, "tool": "get_lease_details", "args": {"lease_id": 1}},
]


async def main():
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(ROOT / "mcp_server" / "server.py")],
    )
    results = []
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tool_list = await session.list_tools()
            tool_names = [t.name for t in tool_list.tools]

            for call in CALLS:
                result = await session.call_tool(call["tool"], call["args"])
                content = [
                    json.loads(c.text) if c.type == "text" else str(c)
                    for c in result.content
                ]
                results.append(
                    {
                        "ticket": call["ticket"],
                        "tool": call["tool"],
                        "args": call["args"],
                        "result": content[0] if len(content) == 1 else content,
                        "is_error": result.isError,
                    }
                )

    output = {
        "tested_at": datetime.datetime.now().astimezone().isoformat(),
        "server": "mcp_server/server.py",
        "database": "data/campus_customs_new.db",
        "tools_registered": tool_names,
        "calls": results,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(output, indent=2))
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
