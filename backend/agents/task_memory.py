# task_memory.py
import logging
from retriever import add_actions_to_memory, add_summary_to_memory, add_transcript_to_memory

logger = logging.getLogger(__name__)

def store_transcript(transcript: str, meeting_name: str):
    try:
        add_transcript_to_memory(transcript, meeting_name)
    except Exception as e:
        logger.exception("Failed storing transcript: %s", e)

def store_summary(summary: str, meeting_name: str):
    try:
        add_summary_to_memory(summary, meeting_name)
    except Exception as e:
        logger.exception("Failed storing summary: %s", e)

def store_actions(actions, meeting_name: str):
    try:
        add_actions_to_memory(actions, meeting_name)
    except Exception as e:
        logger.exception("Failed storing actions: %s", e)
