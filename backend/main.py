from __future__ import annotations
from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from graph.workflow import build_graph_app
from pathlib import Path
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

load_dotenv()

# Frontend paths
FRONTEND_DIR = Path(__file__).parent.parent / "frontend"
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

# Mount static files for CSS and JS
app.mount("/css", StaticFiles(directory=str(FRONTEND_DIR / "css")), name="css")
app.mount("/js", StaticFiles(directory=str(FRONTEND_DIR / "js")), name="js")


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: Optional[str] = None


# API Routes
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - serves index.html"""
    return FileResponse(path=str(FRONTEND_DIR / "index.html"))


@app.get("/chat.html", tags=["Root"])
async def chat_page():
    """Chat page endpoint - serves chat.html"""
    return FileResponse(path=str(FRONTEND_DIR / "chat.html"))


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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0")
