import os
from dotenv import load_dotenv
from fastapi import FastAPI
from app.api.routers import ingest, query  # Importación de routers para endpoints

#Cargar variables de entorno
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key is None:
    raise RuntimeError("❗ La variable de entorno OPENAI_API_KEY no está configurada.")

#Inicialización de la aplicación FastAPI
app = FastAPI(
    title="Konecto QA Microservice",
    description="Microservicio de QA con RAG y OpenAI LLM para consultar documentos PDF.",
    version="1.0.0",
)

#Registro de routers
app.include_router(ingest.router, prefix="/api", tags=["Ingestion"])
app.include_router(query.router, prefix="/api", tags=["Query"])

#Endpoint de salud
@app.get("/", summary="Verificar estado del servicio")
async def read_root():
    """
    Punto de comprobación para validar que el microservicio está operativo.
    """
    return {
        "status": "ok",
        "message": "Konecto QA Microservice está en funcionamiento. Accede a /docs para ver la documentación."
    }

#Inicio de servidor ASGI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )
