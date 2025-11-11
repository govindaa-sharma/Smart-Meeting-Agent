# backend/agents/action_items.py

import google.generativeai as genai

def extract_action_items(transcript: str):
    """
    Extract actionable tasks from the meeting transcript and return them
    as a clean list of bullet points.
    """
    prompt = f"""
    Extract only the clear, concise ACTION ITEMS from the meeting transcript.
    Return them as bullet points. No explanation. No summary.
    
    Transcript:
    {transcript}
    """

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)

    if not response.text:
        return []

    # convert into list
    lines = [line.strip("-• ").strip() for line in response.text.split("\n") if line.strip()]
    return lines
