from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate

from llm import get_llm


async def handle_order_query(query: str) -> str:
    """
    Handle order-related questions (order status, cancellations, returns, modifications).
    """
    llm = get_llm()

    prompt = ChatPromptTemplate.from_template(
        """
You are an Order Support expert for an e-commerce platform.

Your expertise includes:
- Order status and tracking
- Order cancellations and modifications
- Return and refund processes
- Order history inquiries
- Product availability
- Bulk orders and special requests

Customer question:
{query}

Provide a helpful, clear, and concise answer. If you need an order number or specific details 
to help further, politely ask the customer to provide them.
""".strip()
    )

    chain = prompt | llm
    result = await chain.ainvoke({"query": query})
    return result.content.strip()




