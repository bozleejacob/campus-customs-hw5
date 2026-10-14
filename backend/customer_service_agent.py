"""Customer Service: drafts messages for customers. Never sends them."""

from __future__ import annotations

from pathlib import Path

from pydantic_ai import Agent

from .config import get_model, get_model_settings
from .mcp_toolset import get_shop_toolset
from .team import make_delegate_tool, register_agent

NAME = "customer_service"
PROMPT_PATH = Path(__file__).resolve().parent / "prompts" / "customer_service.md"

customer_service_agent = Agent(
    get_model(),
    instructions=PROMPT_PATH.read_text(),
    model_settings=get_model_settings(),
    tools=[make_delegate_tool(NAME)],
    toolsets=[get_shop_toolset(NAME)],
    name=NAME,
)

register_agent(NAME, customer_service_agent)
