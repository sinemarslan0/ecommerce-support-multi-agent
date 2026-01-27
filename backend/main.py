from __future__ import annotations

import asyncio
from typing import NoReturn, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from graph.workflow import build_graph_app


load_dotenv()
graph_app = build_graph_app()

app = FastAPI(
    title="Ecommerce Support Multi-Agent API",
    description="FastAPI backend for the multi-agent customer support system.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Schemas

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: Optional[str] = None


# API Routes

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest) -> ChatResponse:
    """
    Chat endpoint used by the frontend.

    Expects JSON: {"message": "...", "conversation_id": "..."}
    Returns JSON: {"response": "...", "conversation_id": "..."}
    """
    if not payload.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    try:
        state = await graph_app.ainvoke(
            {
                "query": payload.message,
                "conversation_id": payload.conversation_id,
            }
        )
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    final_response = (
        (state or {}).get("final_response")
        or "Sorry, I could not generate a response."
    )

    return ChatResponse(
        response=final_response,
        conversation_id=payload.conversation_id,
    )


# Optional: CLI chat loop (for local testing)

async def chat_loop() -> NoReturn:
    """
    Simple CLI chat loop to interact with the multi-agent support system.
    Type 'exit' or 'quit' to stop.
    """
    print("Multi-Agent Customer Support (FastAPI + LangGraph)")
    print("Type 'exit' or 'quit' to end.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        state = await graph_app.ainvoke({"query": user_input})
        final_response = state.get("final_response") or "Sorry, I could not generate a response."
        print(f"Bot: {final_response}\n")


def main() -> None:
    asyncio.run(chat_loop())


if __name__ == "__main__":
    main()
