import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from app.core.config import settings, CHROMA_DB_PATH

def get_openai_embeddings():
    # Esta es la forma más robusta y explícita de pasar la clave
    return OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY)

def get_chat_openai_llm():
    """Retorna una instancia del LLM de Chat de OpenAI."""
    # Esta es la forma más robusta y explícita de pasar la clave Y el modelo
    return ChatOpenAI(api_key=settings.OPENAI_API_KEY, model_name="gpt-3.5-turbo", temperature=0.5)

def get_chroma_vector_store():
    """Retorna una instancia persistente de Chroma DB."""
    os.makedirs(CHROMA_DB_PATH, exist_ok=True)
    embeddings = get_openai_embeddings()
    return Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)