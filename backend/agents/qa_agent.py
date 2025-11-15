# qa_agent.py
import os
import logging
import google.generativeai as genai
from retriever import retrieve, get_vector_store

logger = logging.getLogger(__name__)
MODEL_NAME = "gemini-2.5-flash"

def _ensure_api_key():
    if not os.getenv("GOOGLE_API_KEY"):
        raise RuntimeError("GOOGLE_API_KEY not set")
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def answer_question(query: str, meeting_name: str) -> str:
    if not query or not meeting_name:
        return "Missing meeting or question."

    # Get memory text (may be empty)
    memory = retrieve(query, meeting_name, k=6) or ""
    # Also check if a vector store exists at all (helps to give better message)
    has_vs = bool(get_vector_store(meeting_name))

    # Build robust prompt:
    prompt_parts = []
    prompt_parts.append("You are an assistant that answers user questions using ONLY the provided meeting memory and summary.")
    prompt_parts.append("If the exact information is not present, say 'I don't have enough info about that in this meeting.' Do NOT invent facts.")
    prompt_parts.append("")
    if memory:
        prompt_parts.append("RELEVANT MEMORY (most relevant chunks first):")
        prompt_parts.append(memory)
    else:
        prompt_parts.append("[No memory found for this meeting]")

    prompt_parts.append("")
    prompt_parts.append("USER QUESTION:")
    prompt_parts.append(query)
    prompt = "\n".join(prompt_parts)

    try:
        _ensure_api_key()
        model = genai.GenerativeModel(MODEL_NAME)
        resp = model.generate_content(prompt)
        text = getattr(resp, "text", "") or ""
        if not text.strip():
            if not has_vs:
                return "No memory exists for this meeting."
            return "I don't have enough info about that in this meeting."
        return text.strip()
    except Exception as e:
        logger.exception("QA generation failed: %s", e)
        return "Failed to generate answer due to an internal error."
