"""Accounting: watches cash and invoices, checks margins, prepares payments for approval."""

from __future__ import annotations

from pathlib import Path

from pydantic_ai import Agent

from .config import get_model, get_model_settings
from .mcp_toolset import get_shop_toolset
from .team import make_delegate_tool, register_agent

NAME = "accounting"
PROMPT_PATH = Path(__file__).resolve().parent / "prompts" / "accounting.md"

accounting_agent = Agent(
    get_model(),
    instructions=PROMPT_PATH.read_text(),
    model_settings=get_model_settings(),
    tools=[make_delegate_tool(NAME)],
    toolsets=[get_shop_toolset(NAME)],
    name=NAME,
)

register_agent(NAME, accounting_agent)
