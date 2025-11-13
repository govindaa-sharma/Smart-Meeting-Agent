from langchain_community.embeddings import HuggingFaceEmbeddings

def embedding_model():
    model_name = "all-MiniLM-L6-v2"  
    return HuggingFaceEmbeddings(model_name=model_name)
