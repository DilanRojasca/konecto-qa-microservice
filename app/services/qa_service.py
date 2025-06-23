from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from app.core.config import settings
from typing import List, Dict, Any

class QAService:
    """
    Servicio de Recuperación Aumentada por Generación (RAG).
    Gestiona la recuperación de contexto relevante y la generación de respuestas
    con un modelo de lenguaje.
    """

    def __init__(self, vector_store: Chroma, llm: ChatOpenAI):
        self.vector_store = vector_store
        self.llm = llm
        # Embeddings para consultas, utilizando la clave de API configurada
        self.embeddings_model = OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY)

    async def get_rag_response(self, query: str) -> Dict[str, Any]:
        """
        Ejecuta una consulta RAG: recupera documentos relevantes y genera una respuesta.
        Retorna un dict con 'answer' y 'sources'.
        """
        # Configura el retriever con más documentos para mejorar la cobertura
        retriever = self.vector_store.as_retriever(search_kwargs={"k": 6})

        # Plantilla del prompt para condicionar la respuesta en base al contexto
        prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "Responde la pregunta basándote exclusivamente en este contexto.\n"
                "Si la información no está presente, indícalo de forma amable.\n"
                "Contexto:\n{context}"
            )),
            ("user", "{input}")
        ])

        # Crear la cadena RAG combinada de recuperación + generación
        doc_chain = create_stuff_documents_chain(self.llm, prompt)
        retrieval_chain = create_retrieval_chain(retriever, doc_chain)

        # Ejecutar la consulta
        response = retrieval_chain.invoke({"input": query})

        # Extraer respuesta y documentos del resultado
        answer: str = response["answer"]
        retrieved_docs: List[Document] = response["context"]

        # Formatear las fuentes recuperadas
        sources = []
        for doc in retrieved_docs:
            doc_name = doc.metadata.get("source", "desconocido")
            page = doc.metadata.get("page")
            sources.append({
                "document": doc_name,
                "page": page if isinstance(page, int) else None,
                "snippet": doc.page_content
            })

        # Eliminar fuentes duplicadas
        unique_sources = []
        seen = set()
        for src in sources:
            key = (src["document"], src["page"])
            if key not in seen:
                unique_sources.append(src)
                seen.add(key)

        return {"answer": answer, "sources": unique_sources}
