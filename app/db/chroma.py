import os
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings # Necesitamos la clase para el embedding_function
from app.core.config import settings, CHROMA_DB_PATH # Importa settings y CHROMA_DB_PATH
# Esta función es un wrapper simple que llama a la dependencia,
# o podría contener lógica de inicialización específica de la DB si fuera más compleja.
def get_chroma_client():
    """
    Inicializa y devuelve una instancia de Chroma DB.
    Se asegura de que el directorio de persistencia exista.
    """
    os.makedirs(CHROMA_DB_PATH, exist_ok=True)
    # CAMBIO AQUÍ: Usar 'api_key=' en lugar de 'openai_api_key='
    embeddings_model = OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY)
    db = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings_model)
    return db

def clear_chroma_db():
    """
    Elimina todos los archivos persistentes de ChromaDB del directorio CHROMA_DB_PATH.
    Esto efectivamente "limpia" la base de datos vectorial.
    """
    if os.path.exists(CHROMA_DB_PATH):
        import shutil
        shutil.rmtree(CHROMA_DB_PATH)
        print(f"Directorio de ChromaDB '{CHROMA_DB_PATH}' eliminado exitosamente.")
    else:
        print(f"El directorio de ChromaDB '{CHROMA_DB_PATH}' no existe, no hay nada que limpiar.")
    # Asegurarse de que el directorio se recree para futuras operaciones
    os.makedirs(CHROMA_DB_PATH, exist_ok=True)