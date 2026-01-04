from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate

from llm import get_llm


async def handle_account_query(query: str) -> str:
    """
    Handle account-related questions (login, password, profile, account settings).
    """
    llm = get_llm()

    prompt = ChatPromptTemplate.from_template(
        """
You are an Account Support expert for an e-commerce platform.

Your expertise includes:
- Account creation and login issues
- Password reset and security
- Profile and account settings
- Email verification
- Two-factor authentication
- Account deletion requests

Customer question:
{query}

Provide a helpful, clear, and concise answer. If you need specific account details to help further, 
politely ask the customer to provide them or suggest contacting support with their account information.
""".strip()
    )

    chain = prompt | llm
    result = await chain.ainvoke({"query": query})
    return result.content.strip()




