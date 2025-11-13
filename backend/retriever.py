import os
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

model_name = "all-MiniLM-L6-v2"  
emb = HuggingFaceEmbeddings(model_name=model_name)

VECTOR_STORE_DIR = "data/vector_store"
os.makedirs(VECTOR_STORE_DIR, exist_ok=True)


def get_vector_store(meeting_name: str):
    path = f"{VECTOR_STORE_DIR}/actions_{meeting_name}"
    if os.path.exists(path):
        return FAISS.load_local(path, emb, allow_dangerous_deserialization=True)
    return None


def add_to_memory(text: str, meeting_name: str):
    vs = get_vector_store(meeting_name)
    if vs is None:
        vs = FAISS.from_texts([text], emb)
    else:
        vs.add_texts([text])
    vs.save_local(f"{VECTOR_STORE_DIR}/actions_{meeting_name}")


def retrieve(query: str, meeting_name: str) -> str:
    vs = get_vector_store(meeting_name)
    if not vs:
        return "No memory found for this meeting yet."
    result = vs.similarity_search(query, k=3)
    return "\n".join([doc.page_content for doc in result])
