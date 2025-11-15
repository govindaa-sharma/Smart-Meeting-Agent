import os
import logging
import google.generativeai as genai

logger = logging.getLogger(__name__)
MODEL_NAME = "gemini-2.5-flash"

def _ensure_api_key():
    if not os.getenv("GOOGLE_API_KEY"):
        raise RuntimeError("GOOGLE_API_KEY not set")
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def extract_action_items(transcript: str):
    """
    Use the LLM to extract action items. Returns a list of action strings.
    """
    if not transcript or not isinstance(transcript, str):
        return []

    
    if len(transcript) > 20000:
        transcript = transcript[-20000:]

    prompt = (
        "Extract clear ACTION ITEMS from the meeting transcript. "
        "Return each action on its own line as: Person: action (deadline if present). "
        "Return only the list items, no extra explanation.\n\n"
        f"Transcript:\n{transcript}"
    )
    try:
        _ensure_api_key()
        model = genai.GenerativeModel(MODEL_NAME)
        resp = model.generate_content(prompt)
        text = getattr(resp, "text", "") or ""
        lines = []
        for raw in text.splitlines():
            s = raw.strip()
            if not s:
                continue
            s = s.lstrip("-•0123456789. )\t").strip()
            if s:
                lines.append(s)
        return lines
    except Exception as e:
        logger.exception("Action extraction failed: %s", e)
        return []
