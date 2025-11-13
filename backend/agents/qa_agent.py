import google.generativeai as genai
import os
from retriever import retrieve

def answer_question(query: str, meeting_name: str):
    # 1. retrieve relevant memory
    context = retrieve(query, meeting_name)

    prompt = f"""
You are an AI assistant helping explain the details of a meeting.

MEETING NAME: {meeting_name}

USER QUESTION:
{query}

RELEVANT CONTEXT FROM MEETING MEMORY:
{context}

Using ONLY the above context, answer the question clearly.
If the context doesn't contain enough information, say:
"I don't have enough info about that in this meeting."
    """

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)

    try:
        return response.text
    except:
        return "No valid response was generated."
