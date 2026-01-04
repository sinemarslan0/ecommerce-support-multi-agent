from __future__ import annotations
from typing import Literal
from langgraph.graph import END, StateGraph

from agents.account_agent import handle_account_query
from agents.delivery_agent import handle_delivery_query
from agents.order_agent import handle_order_query
from agents.payment_agent import handle_payment_query
from agents.router import route_query
from agents.synthesizer import synthesize_response
from graph.state import AgentState


async def router_node(state: AgentState) -> AgentState:
    assert "query" in state and state["query"], "Router node requires 'query' in state."
    route = await route_query(state["query"])
    return {**state, "route": route}


async def order_node(state: AgentState) -> AgentState:
    assert state.get("query"), "Order node requires 'query' in state."
    expert_response = await handle_order_query(state["query"])
    return {**state, "expert_response": expert_response}


async def delivery_node(state: AgentState) -> AgentState:
    assert state.get("query"), "Delivery node requires 'query' in state."
    expert_response = await handle_delivery_query(state["query"])
    return {**state, "expert_response": expert_response}


async def payment_node(state: AgentState) -> AgentState:
    assert state.get("query"), "Payment node requires 'query' in state."
    expert_response = await handle_payment_query(state["query"])
    return {**state, "expert_response": expert_response}


async def account_node(state: AgentState) -> AgentState:
    assert state.get("query"), "Account node requires 'query' in state."
    expert_response = await handle_account_query(state["query"])
    return {**state, "expert_response": expert_response}


async def synthesizer_node(state: AgentState) -> AgentState:
    assert state.get("query") and state.get(
        "expert_response"
    ), "Synthesizer node requires 'query' and 'expert_response' in state."
    final_response = await synthesize_response(state["query"], state["expert_response"])  # type: ignore[arg-type]
    return {**state, "final_response": final_response}


def _route_to_expert(state: AgentState) -> Literal["order", "delivery", "payment", "account"]:
    """
    LangGraph conditional edge function. It reads `state["route"]` and
    returns the name of the next node.
    """
    route = state.get("route") or "order"
    if route not in {"order", "delivery", "payment", "account"}:
        route = "order"
    return route  # type: ignore[return-value]


def build_graph_app():
    """
    Build and compile the LangGraph workflow:

    query -> router -> (order|delivery|payment|account) -> synthesizer -> END
    """
    workflow = StateGraph(AgentState)

    # Register nodes
    workflow.add_node("router", router_node)
    workflow.add_node("order", order_node)
    workflow.add_node("delivery", delivery_node)
    workflow.add_node("payment", payment_node)
    workflow.add_node("account", account_node)
    workflow.add_node("synthesizer", synthesizer_node)

    # Entry point
    workflow.set_entry_point("router")

    # Conditional routing from router to the appropriate expert
    workflow.add_conditional_edges(
        "router",
        _route_to_expert,
        {
            "order": "order",
            "delivery": "delivery",
            "payment": "payment",
            "account": "account",
        },
    )

    # Each expert goes to the synthesizer
    workflow.add_edge("order", "synthesizer")
    workflow.add_edge("delivery", "synthesizer")
    workflow.add_edge("payment", "synthesizer")
    workflow.add_edge("account", "synthesizer")

    # Synthesizer is the final step
    workflow.add_edge("synthesizer", END)

    app = workflow.compile()
    return app




