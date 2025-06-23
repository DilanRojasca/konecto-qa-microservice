from fastapi import APIRouter, Depends
from app.models.schemas import QueryRequest, QueryResponse # Importa los schemas
from app.services.qa_service import QAService # ¡Ajustado a qa_service!
from app.core.dependencies import get_chroma_vector_store, get_chat_openai_llm # Dependencias para el LLM y Vector Store
from app.core.exceptions import QueryProcessingError # Importa la excepción personalizada

# Importaciones para tipado
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI

# Inicializa un APIRouter específico para consultas.
router = APIRouter()

@router.post(
    "/query",
    response_model=QueryResponse, # Indica el esquema de la respuesta esperada
    summary="Consultar los documentos ingestados con una pregunta",
    description="Recibe una pregunta del usuario, busca información relevante en los documentos "
                "ingestados y genera una respuesta utilizando un modelo de lenguaje grande (LLM)."
)
async def query_documents(
    request: QueryRequest,
    vector_store: Chroma = Depends(get_chroma_vector_store),
    llm: ChatOpenAI = Depends(get_chat_openai_llm)
) -> QueryResponse:
    qa_service = QAService(vector_store, llm)

    try:
        # Aquí, qa_service.get_rag_response() ahora devuelve un dict con 'answer' y 'sources'
        # que coincide directamente con el QueryResponse.
        response_data = await qa_service.get_rag_response(request.query)
        return QueryResponse(**response_data) # Desempaqueta el dict para crear el objeto QueryResponse
    except Exception as e:
        raise QueryProcessingError(detail=f"Error interno al procesar la consulta: {str(e)}")