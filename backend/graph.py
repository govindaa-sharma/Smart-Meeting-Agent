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
from agents.qa_agent import answer_question
from retriever import retrieve


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
    summary = summarize_meeting(state["transcript"])
    return {"summary": summary}


def actions_node(state: MeetingState):
    actions = extract_action_items(state["transcript"])

    if not actions or not isinstance(actions, list):
        actions = []

    if actions:
        store_action_items(actions, state["title"])

    return {"actions": actions}


def memory_node(state: MeetingState):
    memory_output = retrieve("important actions", state["title"])
    return {"memory": memory_output}



workflow = StateGraph(MeetingState)
workflow.add_node("summarize", summarize_node)
workflow.add_node("actions", actions_node)
workflow.add_node("memory", memory_node)

workflow.set_entry_point("summarize")
workflow.add_edge("summarize", "actions")
workflow.add_edge("actions", "memory")
workflow.add_edge("memory", END)

workflow = workflow.compile()



def qa_node(state: QAState):
    query = state.get("query", "")
    title = state.get("title", "")
    answer = answer_question(query, title)
    return {"answer": answer}

qa_graph = StateGraph(QAState)
qa_graph.add_node("qa", qa_node)
qa_graph.set_entry_point("qa")
qa_graph = qa_graph.compile()
