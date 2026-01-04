from __future__ import annotations
import asyncio
from typing import NoReturn
from dotenv import load_dotenv
from graph.workflow import build_graph_app

async def chat_loop() -> NoReturn:
    """
    Simple CLI chat loop to interact with the multi-agent support system.
    Type 'exit' or 'quit' to stop.
    """
    load_dotenv()

    app = build_graph_app()

    print("Multi-Agent Customer Support (LangGraph + llama-3.1-8b-instant via Groq)")
    print("Type 'exit' or 'quit' to end.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        # Invoke the graph and get the final state
        state = await app.ainvoke({"query": user_input})

        final_response = state.get("final_response") or "Sorry, I could not generate a response."
        print(f"Bot: {final_response}\n")


def main() -> None:
    asyncio.run(chat_loop())


if __name__ == "__main__":
    main()



