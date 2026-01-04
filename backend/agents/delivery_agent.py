from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate

from llm import get_llm


async def handle_delivery_query(query: str) -> str:
    """
    Handle delivery and shipping-related questions (shipping times, tracking, delivery issues).
    """
    llm = get_llm()

    prompt = ChatPromptTemplate.from_template(
        """
You are a Delivery & Shipping Support expert for an e-commerce platform.

Your expertise includes:
- Shipping methods and delivery times
- Package tracking and location
- Delivery delays and issues
- International shipping
- Shipping costs and free shipping thresholds
- Lost or damaged packages
- Address changes before delivery

Customer question:
{query}

Provide a helpful, clear, and concise answer. If you need a tracking number or order details 
to help further, politely ask the customer to provide them.
""".strip()
    )

    chain = prompt | llm
    result = await chain.ainvoke({"query": query})
    return result.content.strip()




