"""Campus Customs agent team.

Importing this package wires up all five agents and registers them with
`team.AGENT_REGISTRY`, so `delegate(to_agent, task)` can reach any of them
from any of them (full connectivity).
"""

from .accounting_agent import accounting_agent
from .boss_agent import boss_agent
from .customer_service_agent import customer_service_agent
from .facilities_agent import facilities_agent
from .inventory_agent import inventory_agent

__all__ = [
    "boss_agent",
    "inventory_agent",
    "accounting_agent",
    "facilities_agent",
    "customer_service_agent",
]
