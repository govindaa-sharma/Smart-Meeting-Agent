# summarizer.py
import os
import logging
import google.generativeai as genai

logger = logging.getLogger(__name__)
MODEL_NAME = "gemini-2.5-flash"

def _ensure_api_key():
    if not os.getenv("GOOGLE_API_KEY"):
        raise RuntimeError("GOOGLE_API_KEY not set")
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def summarize_meeting(transcript: str) -> str:
    if not transcript or not isinstance(transcript, str):
        return "No transcript provided."

    if len(transcript) > 20000:
        transcript = transcript[-20000:]

    prompt = (
        "Summarize the following meeting transcript into a concise, structured summary "
        "that includes decisions, deadlines, owners, and important notes.\n\n"
        f"Transcript:\n{transcript}"
    )

    try:
        _ensure_api_key()
        model = genai.GenerativeModel(MODEL_NAME)
        resp = model.generate_content(prompt)
        text = getattr(resp, "text", "") or ""
        return text.strip() if text.strip() else "No summary generated."
    except Exception as e:
        logger.exception("Summarization failed: %s", e)
        return "Failed to generate summary."
