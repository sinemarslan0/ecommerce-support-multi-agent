from __future__ import annotations
from typing import Literal
from langchain_core.prompts import ChatPromptTemplate
from llm import get_llm

RouterLabel = Literal["order", "delivery", "payment", "account"]


async def route_query(query: str) -> RouterLabel:
    """
    Classify the user query into one of the expert domains.

    Possible labels:
    - 'order'    : returns, cancellations, order status
    - 'delivery' : shipping, tracking, delivery times
    - 'payment'  : payment methods, billing issues, refunds
    - 'account'  : login, password, profile/account settings
    """
    llm = get_llm()

    prompt = ChatPromptTemplate.from_template(
        """
You are a classifier that reads a customer message and decides which support expert 
should handle it. You must answer with ONE WORD ONLY from this list:

- order
- delivery
- payment
- account

Customer message:
{query}

Answer with exactly one of: order, delivery, payment, account.
""".strip()
    )

    chain = prompt | llm
    result = await chain.ainvoke({"query": query})
    label = result.content.strip().lower()

    # Basic fallback to keep the graph running even if the model answers creatively.
    if label not in {"order", "delivery", "payment", "account"}:
        label = "order"

    return label  # type: ignore[return-value]




