# retriever.py
import os
import logging
from dotenv import load_dotenv
load_dotenv()

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)

# Embedding model used for FAISS
EMB_MODEL = "all-MiniLM-L6-v2"
emb = HuggingFaceEmbeddings(model_name=EMB_MODEL)

# storage paths
VECTOR_STORE_ROOT = "data/vector_store"
os.makedirs(VECTOR_STORE_ROOT, exist_ok=True)

# chunking config
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

def _vs_folder(meeting_name: str) -> str:
    safe = "".join(c for c in meeting_name if c.isalnum() or c in (" ", "_", "-")).strip()
    return os.path.join(VECTOR_STORE_ROOT, f"actions_{safe}")

def get_vector_store(meeting_name: str):
    """
    Load FAISS vectorstore for given meeting, or return None if not present or loading fails.
    """
    folder = _vs_folder(meeting_name)
    if not os.path.isdir(folder):
        return None
    try:
        vs = FAISS.load_local(folder, emb, allow_dangerous_deserialization=True)
        return vs
    except Exception as e:
        logger.exception("Failed to load FAISS store at %s: %s", folder, e)
        return None

def save_vector_store(vs, meeting_name: str):
    folder = _vs_folder(meeting_name)
    os.makedirs(folder, exist_ok=True)
    vs.save_local(folder)
    logger.debug("Saved vector store at %s", folder)

def add_transcript_to_memory(transcript: str, meeting_name: str):
    """
    Split transcript into chunks and add to vectorstore, prefixing chunks with a tag to indicate source.
    This ensures queries can retrieve transcript content as part of RAG.
    """
    if not transcript or not meeting_name:
        logger.warning("add_transcript_to_memory called with empty data.")
        return

    texts = splitter.split_text(transcript)
    # tag each transcript chunk so we can identify it in retrieval if necessary
    tagged = [f"TRANSCRIPT: {t}" for t in texts]

    folder = _vs_folder(meeting_name)
    vs = get_vector_store(meeting_name)
    try:
        if vs is None:
            vs = FAISS.from_texts(tagged, emb)
        else:
            vs.add_texts(tagged)
        save_vector_store(vs, meeting_name)
    except Exception as e:
        logger.exception("Failed to add transcript to memory for %s: %s", meeting_name, e)
        raise

def add_summary_to_memory(summary: str, meeting_name: str):
    """
    Add summary as a single chunk (tagged).
    """
    if not summary or not meeting_name:
        logger.debug("No summary to store for %s", meeting_name)
        return

    tagged = [f"SUMMARY: {summary.strip()}"]
    vs = get_vector_store(meeting_name)
    try:
        if vs is None:
            vs = FAISS.from_texts(tagged, emb)
        else:
            vs.add_texts(tagged)
        save_vector_store(vs, meeting_name)
    except Exception as e:
        logger.exception("Failed to add summary for %s: %s", meeting_name, e)
        raise

def add_actions_to_memory(actions, meeting_name: str):
    """
    actions may be a list or string. Add to memory as tagged chunks.
    """
    if not actions or not meeting_name:
        logger.debug("No actions to store for %s", meeting_name)
        return

    if isinstance(actions, list):
        texts = [f"ACTION: {a}" for a in actions if a]
    else:
        texts = [f"ACTION: {actions}"]

    vs = get_vector_store(meeting_name)
    try:
        if vs is None:
            vs = FAISS.from_texts(texts, emb)
        else:
            vs.add_texts(texts)
        save_vector_store(vs, meeting_name)
    except Exception as e:
        logger.exception("Failed to add actions for %s: %s", meeting_name, e)
        raise

def retrieve(query: str, meeting_name: str, k: int = 5) -> str:
    """
    Run similarity search across the combined memory for the meeting and return a concatenated string.
    If nothing exists, return an explanatory string.
    """
    vs = get_vector_store(meeting_name)
    if not vs:
        return ""  # empty string => no memory

    try:
        docs = vs.similarity_search(query, k=k)
        pieces = []
        for d in docs:
            # unified retrieval: use page_content when available, else str(doc)
            txt = getattr(d, "page_content", None)
            if txt is None:
                txt = str(d)
            pieces.append(txt)
        # Join selected pieces with separators so the LLM sees clear boundaries
        return "\n\n---\n\n".join(pieces)
    except Exception as e:
        logger.exception("Similarity search failed for %s: %s", meeting_name, e)
        return ""
