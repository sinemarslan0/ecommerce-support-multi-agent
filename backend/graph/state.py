from __future__ import annotations
from typing import Literal, Optional, TypedDict

class AgentState(TypedDict, total=False):
    """
    Shared state passed between nodes in the LangGraph workflow.

    - query: the raw user message
    - route: which expert should handle the query
    - expert_response: raw response from the selected expert agent
    - final_response: polished answer from the synthesizer agent
    """

    query: str
    route: Optional[Literal["order", "delivery", "payment", "account"]]
    expert_response: Optional[str]
    final_response: Optional[str]




