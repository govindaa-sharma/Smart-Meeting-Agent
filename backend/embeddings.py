# embeddings.py
from langchain_community.embeddings import HuggingFaceEmbeddings

def embedding_model():
    """
    Return an embeddings object. Keep the model name configurable if required.
    """
    model_name = "all-MiniLM-L6-v2"
    return HuggingFaceEmbeddings(model_name=model_name)
