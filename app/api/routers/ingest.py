from typing import List # Define el tipo 'List' para listas.
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status # Componentes de FastAPI.
from app.services.document_service import DocumentService # Servicio de lógica de negocio para documentos.
from app.core.dependencies import get_chroma_vector_store, get_openai_embeddings # Funciones para inyectar dependencias.
from app.db.chroma import clear_chroma_db
# Importaciones específicas de LangChain.
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# Inicializa el router de FastAPI para organizar los endpoints.
router = APIRouter()

# Define el endpoint POST para la ingesta de documentos.
@router.post(
    "/clear_db",
    summary="Limpia la base de datos vectorial Chroma DB",
    description="Cuidado! esta accion es irreversible y borrara todos los datos de forma permanente",
    status_code=status.HTTP_200_OK,
)
async def clear_database() -> dict: #Retorna un diccionario simple para la confirmacion
    """"Endpoint para limpiar la base de datos"""
    try:
        clear_chroma_db() #Llama a la funcion de limpieza implementada en app.db.chroma
        return {"message": "Base de datos eliminada correctamente"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error procesando {e.__class__.__name__}: {str(e)}"
        )
@router.post("/ingest", summary="Ingestar uno o más archivos PDF y generar embeddings")
async def ingest_documents(
    # Parámetro para recibir una lista de archivos subidos en formato de formulario.
    files: List[UploadFile] = File(
        ...,
        description="Lista de archivos PDF a ingestar."
    ),
    # Inyecta la instancia del vector store Chroma a través de una dependencia.
    vector_store: Chroma = Depends(get_chroma_vector_store),
    # Inyecta la instancia del modelo de embeddings de OpenAI a través de una dependencia.
    embeddings_model: OpenAIEmbeddings = Depends(get_openai_embeddings)
) -> dict:
    """
    Procesa PDFs subidos, extrae texto, genera embeddings y los almacena en Chroma DB.
    """
    # Crea una instancia del DocumentService, pasándole las dependencias necesarias.
    document_service = DocumentService(vector_store, embeddings_model)
    total_ingested_chunks = 0 # Contador para el total de fragmentos procesados.

    # Itera sobre cada archivo en la lista de archivos subidos.
    for file in files:
        # Valida que el archivo subido sea un PDF.
        if not file.filename.endswith(".pdf"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El archivo '{file.filename}' no es un PDF. Solo se aceptan archivos .pdf"
            )
        try:
            # Llama al servicio para procesar el PDF y obtener el número de fragmentos.
            num_chunks = await document_service.ingest_pdf(file)
            total_ingested_chunks += num_chunks # Suma los fragmentos al total.
        except Exception as e:
            # Captura y maneja errores durante el procesamiento de un archivo individual.
            print(f"Error procesando {file.filename}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al procesar el archivo '{file.filename}': {str(e)}"
            )


    # Retorna la cantidad total de fragmentos de documentos ingestados.
    return {"ingested_documents": total_ingested_chunks}