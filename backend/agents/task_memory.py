# backend/agents/task_memory.py

from retriever import add_to_memory

def store_action_items(actions, meeting_name: str):
    """
    Saves extracted action items into memory storage.
    """
    text = "\n".join(actions)
    add_to_memory(text, f"actions_{meeting_name}")
