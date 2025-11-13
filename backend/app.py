from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from graph import workflow
import shutil
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload_meeting")
async def upload_meeting(title: str, file: UploadFile = File(...)):
    path = f"data/meetings/{title}.txt"
    raw_path = f"data/meetings/raw_{title}.txt"

    with open(raw_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    with open(raw_path, "r", encoding="utf-8") as f:
        transcript = f.read()

    result = workflow.invoke({"title": title, "transcript": transcript})

    with open(path, "w", encoding="utf-8") as f:
        f.write(result["summary"])

    import json
    actions_path = f"data/vector_store/actions_{title}.json"
    with open(actions_path, "w") as f:
        json.dump(result["actions"], f, indent=2)

    return result

# @app.post("/chat")
# def chat(query: str):
#     result = workflow.invoke({"query": query, "transcript": ""})
#     return {"response": result["memory_recall"]}

import os
from fastapi.responses import JSONResponse

DATA_DIR = "data/meetings"

@app.get("/meetings")
def list_meetings():
    if not os.path.exists(DATA_DIR):
        return []
    files = [f.replace(".txt", "") for f in os.listdir(DATA_DIR) if f.endswith(".txt")]
    return files

@app.get("/meeting/{title}")
def get_meeting_details(title: str):
    meeting_path = os.path.join(DATA_DIR, f"{title}.txt")
    actions_path = os.path.join("data", "vector_store", f"actions_{title}.json")

    summary = "No summary found"
    actions = []

    if os.path.exists(meeting_path):
        with open(meeting_path, "r") as f:
            summary = f.read()

    if os.path.exists(actions_path):
        import json
        with open(actions_path, "r") as f:
            actions = json.load(f)

    return {"title": title, "summary": summary, "actions": actions}

@app.post("/ask")
def ask_question(payload: dict):
    meeting = payload["meeting"]
    question = payload["query"]
    result = workflow.invoke({"title": meeting, "transcript": question})
    return {"response": result["summary"]} 
