# graph.py
import os
from dotenv import load_dotenv
load_dotenv()

import logging
import google.generativeai as genai
genai.configure(api_key=os.getenv("GOOGLE_API_KEY", "") or None)

from langgraph.graph import StateGraph, END
from typing import TypedDict, List

from agents.summarizer import summarize_meeting
from agents.action_items import extract_action_items
from agents.task_memory import store_action_items
from agents.qa_agent import answer_question
from retriever import retrieve

logger = logging.getLogger(__name__)

class MeetingState(TypedDict, total=False):
    title: str
    transcript: str
    summary: str
    actions: List[str]
    memory: str

class QAState(TypedDict, total=False):
    title: str
    query: str
    answer: str

def summarize_node(state: MeetingState):
    transcript = state.get("transcript", "")
    summary = summarize_meeting(transcript)
    return {"summary": summary}

def actions_node(state: MeetingState):
    transcript = state.get("transcript", "")
    title = state.get("title", "")
    actions = extract_action_items(transcript)

    if not actions or not isinstance(actions, list):
        actions = []

    if actions and title:
        try:
            store_action_items(actions, title)
        except Exception as e:
            logger.exception("Failed to store actions for %s: %s", title, e)
    return {"actions": actions}

def memory_node(state: MeetingState):
    title = state.get("title", "")
    try:
        memory_output = retrieve("important actions", title) if title else ""
    except Exception as e:
        logger.exception("Failed to retrieve memory for %s: %s", title, e)
        memory_output = ""
    return {"memory": memory_output}

# build meeting workflow
workflow = StateGraph(MeetingState)
workflow.add_node("summarize", summarize_node)
workflow.add_node("actions", actions_node)
workflow.add_node("memory", memory_node)
workflow.set_entry_point("summarize")
workflow.add_edge("summarize", "actions")
workflow.add_edge("actions", "memory")
workflow.add_edge("memory", END)
workflow = workflow.compile()

# QA graph
def qa_node(state: QAState):
    query = state.get("query", "")
    title = state.get("title", "")
    answer = answer_question(query, title)
    return {"answer": answer}

qa_graph = StateGraph(QAState)
qa_graph.add_node("qa", qa_node)
qa_graph.set_entry_point("qa")
qa_graph = qa_graph.compile()
