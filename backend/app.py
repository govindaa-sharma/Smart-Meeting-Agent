import os
import shutil
import logging
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
load_dotenv()

from agents.summarizer import summarize_meeting
from agents.action_items import extract_action_items
from retriever import add_transcript_to_memory, add_summary_to_memory, add_actions_to_memory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = "data/meetings"
os.makedirs(DATA_DIR, exist_ok=True)

@app.post("/upload_meeting")
async def upload_meeting(title: str, file: UploadFile = File(...)):
    if not title:
        raise HTTPException(status_code=400, detail="title parameter is required")

    safe_title = "".join(c for c in title if c.isalnum() or c in (" ", "_", "-")).strip()
    if not safe_title:
        raise HTTPException(status_code=400, detail="Invalid title after sanitization")

    raw_dir = DATA_DIR
    os.makedirs(raw_dir, exist_ok=True)

    raw_path = os.path.join(raw_dir, f"raw_{safe_title}.txt")
    summary_path = os.path.join(raw_dir, f"{safe_title}.txt")

    try:
        
        with open(raw_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        
        with open(raw_path, "r", encoding="utf-8", errors="replace") as f:
            transcript = f.read()

        
        add_transcript_to_memory(transcript, safe_title)

        
        summary = summarize_meeting(transcript) or ""
        actions = extract_action_items(transcript) or []

        
        add_summary_to_memory(summary, safe_title)
        add_actions_to_memory(actions, safe_title)

        
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(summary)
        print("SUMMARY GENERATED:", summary)


        
        return {"ok": True, "summary": summary, "actions": actions}
    except Exception as e:
        logger.exception("upload_meeting failed for %s: %s", safe_title, e)
        raise HTTPException(status_code=500, detail=f"Failed to process meeting: {e}")

@app.get("/meetings")
def list_meetings():
    try:
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR, exist_ok=True)
            return []

        all_files = os.listdir(DATA_DIR)
        txt_files = [f for f in all_files if f.endswith(".txt")]

        
        final_files = [
            f.replace(".txt", "")
            for f in txt_files
            if not f.startswith("raw_")
        ]

        return final_files

    except Exception as e:
        logger.exception("Failed to list meetings: %s", e)
        return []


from retriever import retrieve

@app.get("/meeting/{title}")
def get_meeting_details(title: str):
    meeting_path = os.path.join(DATA_DIR, f"{title}.txt")
    summary = "No summary found"
    if os.path.exists(meeting_path):
        with open(meeting_path, "r", encoding="utf-8", errors="replace") as f:
            summary = f.read()

    
    actions_memory = retrieve("action", title, k=10)
    actions = []
    if actions_memory:
        for line in actions_memory.splitlines():
            if line.strip().startswith("ACTION:"):
                actions.append(line.replace("ACTION:", "").strip())

    return {"title": title, "summary": summary, "actions": actions}

@app.post("/ask")
def ask_question(payload: dict):
    meeting = payload.get("meeting")
    question = payload.get("query") or payload.get("question")

    if not meeting or not question:
        raise HTTPException(status_code=400, detail="Both 'meeting' and 'query' fields are required.")

    try:
        
        from agents.qa_agent import answer_question
        ans = answer_question(question, meeting)
        return {"response": ans}
    except Exception as e:
        logger.exception("Ask endpoint failed: %s", e)
        raise HTTPException(status_code=500, detail="Failed to answer question.")
