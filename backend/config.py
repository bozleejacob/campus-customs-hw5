"""Shared model and guardrail settings for every Campus Customs agent.

Every agent uses the same Portkey-routed Luna model and the same token/step
guardrails, so no single ticket (or chain of delegations) can run away.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.settings import ModelSettings
from pydantic_ai.usage import UsageLimits

load_dotenv()

MODEL_NAME = "gpt-5.6-luna"

# Token-usage guardrails. These exist so a multi-agent delegation chain can't
# quietly burn an unbounded number of tokens or tool calls on one ticket.
# MAX_TOOL_CALLS_PER_RUN / MAX_TOTAL_TOKENS_PER_RUN were first set to 8/4000,
# but a real ticket resolution (Boss -> Inventory -> Accounting -> Boss ->
# Customer Service, each with its own tool calls) legitimately needs more
# than that — a live run hit the 4000-token ceiling mid-resolution. Raised
# to values with real headroom for that chain, while still capping it well
# short of "unbounded."
MAX_OUTPUT_TOKENS_PER_CALL = 600
MAX_TOOL_CALLS_PER_RUN = 24
MAX_TOTAL_TOKENS_PER_RUN = 20000
MAX_DELEGATION_DEPTH = 2


def get_model() -> OpenAIChatModel:
    api_key = os.environ["PORTKEY_API_KEY"]
    provider = OpenAIProvider(api_key=api_key, base_url="https://api.portkey.ai/v1")
    return OpenAIChatModel(MODEL_NAME, provider=provider)


def get_model_settings() -> ModelSettings:
    return ModelSettings(max_tokens=MAX_OUTPUT_TOKENS_PER_CALL)


def get_usage_limits() -> UsageLimits:
    return UsageLimits(
        request_limit=MAX_TOOL_CALLS_PER_RUN,
        total_tokens_limit=MAX_TOTAL_TOKENS_PER_RUN,
    )
