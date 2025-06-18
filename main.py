import os
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List, Optional

# --- Carga de variables de entorno ---
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key is None:
    raise ValueError("La variable de entorno OPENAI_API_KEY no está configurada.")

# --- Inicialización de FastAPI ---
app = FastAPI(
    title="Konecto QA Microservice",
    description="Microservicio de QA con RAG y OpenAI LLM para documentos PDF.",
    version="1.0.0"
)

# --- Configuración de OpenAI y LangChain (esqueleto inicial) ---
# Aquí es donde configurarías tus modelos y la base de datos.
# Por ahora, solo como placeholders para lo que vendrá.

# from langchain_openai import OpenAIEmbeddings, ChatOpenAI
# from langchain_community.vectorstores import Chroma

# embeddings_model = OpenAIEmbeddings(openai_api_key=openai_api_key)
# llm = ChatOpenAI(openai_api_key=openai_api_key, model_name="gpt-3.5-turbo", temperature=0.5)

# # Ruta para persistir Chroma DB localmente
# CHROMA_DB_PATH = "./chroma_db"
# vector_store = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings_model)


# --- Endpoint de Prueba ---
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Konecto QA Microservice! Go to /docs for API documentation."}

# --- Esqueletos de Endpoints Funcionales ---

@app.post("/ingest")
async def ingest_documents(files: List[UploadFile] = File(...)):
    """
    Recibe uno o más archivos PDF, extrae texto, genera embeddings
    y los almacena en Chroma DB.
    """
    ingested_count = 0
    # Lógica para procesar PDFs, extraer texto, generar embeddings y guardarlos en Chroma DB
    # (Esto será más complejo e implicará LangChain y pypdf)

    # Ejemplo de cómo podrías iterar sobre los archivos:
    # for file in files:
    #     content = await file.read()
    #     # Aquí iría la lógica para procesar 'content'
    #     ingested_count += 1 # Incrementar si se procesa con éxito

    return {"ingested_documents": ingested_count}


@app.get("/query") # Cambiado a GET según la descripción original, aunque POST también sería válido para queries complejas.
async def query_documents(question: str, sources: Optional[bool] = False):
    """
    Responde a una pregunta utilizando los documentos ingeridos.
    Opcionalmente, puede devolver las fuentes.
    """
    answer = "Lo siento, aún no puedo responder a preguntas. ¡Estoy en construcción!"
    found_sources = []

    # Lógica para buscar en Chroma DB, usar el LLM de OpenAI y construir la respuesta
    # (Esto implicará el flujo RAG con LangChain)

    if sources:
        return {"answer": answer, "sources": found_sources}
    return {"answer": answer}