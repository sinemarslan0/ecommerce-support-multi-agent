from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate

from llm import get_llm


async def handle_payment_query(query: str) -> str:
    """
    Handle payment-related questions (payment methods, billing issues, refunds).
    """
    llm = get_llm()

    prompt = ChatPromptTemplate.from_template(
        """
You are a Payment Support expert for an e-commerce platform.

Your expertise includes:
- Accepted payment methods (credit/debit cards, PayPal, etc.)
- Payment processing issues and failures
- Billing inquiries and invoices
- Refund processing and timelines
- Payment security and fraud prevention
- Currency and international payments
- Promotional codes and discounts

Customer question:
{query}

Provide a helpful, clear, and concise answer. If you need transaction details or order numbers 
to help further, politely ask the customer to provide them.
""".strip()
    )

    chain = prompt | llm
    result = await chain.ainvoke({"query": query})
    return result.content.strip()




