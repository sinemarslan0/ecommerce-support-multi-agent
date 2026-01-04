from __future__ import annotations
from langchain_core.prompts import ChatPromptTemplate
from llm import get_llm

async def synthesize_response(user_query: str, expert_response: str) -> str:
    """
    Turn the expert's raw answer into a polite, professional, customer-facing message.
    """
    llm = get_llm()

    prompt = ChatPromptTemplate.from_template(
        """
You are a senior customer support agent.
Your goal is to communicate with empathy, clarity, and professionalism.

Rewrite the expert's technical/raw answer into a friendly final reply.

Guidelines:
- Start with a brief acknowledgement of the customer's situation.
- Clearly answer their question using the expert's content.
- Keep it short and easy to understand.
- If relevant, suggest the next best step.

Customer question:
{user_query}

Expert notes (DO NOT show this section explicitly to the customer):
{expert_response}

Now write the final message to the customer.
""".strip()
    )

    chain = prompt | llm
    result = await chain.ainvoke(
        {"user_query": user_query, "expert_response": expert_response}
    )
    return result.content.strip()




