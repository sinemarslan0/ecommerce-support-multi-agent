from __future__ import annotations

import os
from functools import lru_cache

from langchain_groq import ChatGroq
from langchain_openai import OpenAIEmbeddings


@lru_cache(maxsize=1)
def get_llm() -> ChatGroq:
    """
    Configure a shared ChatGroq instance for all agents.

    This is used by all agents.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not set. Please configure it in your .env file.")

    return ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.2,
        api_key=api_key,
    )


@lru_cache(maxsize=1)
def get_embedding_model() -> OpenAIEmbeddings:
    """
    Configure OpenAI embeddings for future RAG implementation.
    
    This will be used for embedding documents and queries in RAG pipelines.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set. Please configure it in your .env file.")

    return OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=api_key,
    )




