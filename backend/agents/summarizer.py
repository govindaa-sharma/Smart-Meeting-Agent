import google.generativeai as genai

def summarize_meeting(transcript: str) -> str:
    """
    Summarize the full meeting transcript into a clear concise summary.
    """
    prompt = f"""
    Summarize the following meeting transcript into a short, clear, and structured summary.
    Focus on decisions made and important discussion points.

    Transcript:
    {transcript}
    """

    response = genai.GenerativeModel("gemini-2.5-flash").generate_content(prompt)
    return response.text.strip()
