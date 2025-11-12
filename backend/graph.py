import os
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

from langgraph.graph import StateGraph, END
from typing import TypedDict, List

from agents.summarizer import summarize_meeting
from agents.action_items import extract_action_items
from agents.task_memory import store_action_items

from retriever import retrieve


class MeetingState(TypedDict):
    title: str
    transcript: str
    summary: str
    actions: List[str]



def summarize_node(state: MeetingState):
    summary = summarize_meeting(state["transcript"])
    return {"summary": summary}

def actions_node(state: MeetingState):
    actions = extract_action_items(state["transcript"])

    if not actions or not isinstance(actions, list):
        actions = []

    if actions:
        store_action_items(actions, state["title"])

    return {"actions": actions}

def retrieve_node(state: MeetingState):
    memory = retrieve("important actions", state["title"])
    return {"memory": memory}


workflow = StateGraph(MeetingState)

workflow.add_node("summarize", summarize_node)
workflow.add_node("actions", actions_node)

workflow.set_entry_point("summarize")
workflow.add_edge("summarize", "actions")
workflow.add_edge("actions", END)

workflow = workflow.compile()
