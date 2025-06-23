import os
import tempfile
from typing import List
from fastapi import UploadFile

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

from app.core.exceptions import DocumentProcessingError


class DocumentService:
    """
    Servicio para ingesta de PDFs: carga, fragmentación y almacenamiento
    en la base de datos vectorial para su posterior consulta RAG.
    """

    def __init__(self, vector_store: Chroma, embeddings_model: OpenAIEmbeddings):
        """
        Args:
            vector_store (Chroma): almacena los vectores generados.
            embeddings_model (OpenAIEmbeddings): modelo de embeddings (incluso si
                Chroma lo contiene internamente, se mantiene para consistencia).
        """
        self.vector_store = vector_store
        self.embeddings_model = embeddings_model

        # Divider que produce fragmentos coherentes con contexto de solapamiento.
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            is_separator_regex=False,
        )

    async def ingest_pdf(self, file: UploadFile) -> int:
        """
        Lee un archivo PDF, lo fragmenta y agrega sus embeddings a Chroma.

        Args:
            file (UploadFile): PDF recibido desde la API.
        Returns:
            int: número total de fragmentos procesados.
        Raises:
            DocumentProcessingError: error durante cualquier fase de ingestión.
        """
        tmp_file_path = None

        try:
            # Escritura temporal del PDF para que PyPDFLoader pueda leerlo
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                await file.seek(0)
                tmp.write(await file.read())
                tmp_file_path = tmp.name

            # Extracción y división en fragmentos usando LangChain
            loader = PyPDFLoader(tmp_file_path)
            chunks: List[Document] = loader.load_and_split(self.text_splitter)

            # Añadir metadatos para trazabilidad en RAG
            for chunk in chunks:
                chunk.metadata["source"] = file.filename
                chunk.metadata["page"] = chunk.metadata.get("page", "N/A")

            # Inserta los fragmentos en la base vectorial
            self.vector_store.add_documents(chunks)

            print(f"Ingested {len(chunks)} chunks from {file.filename}")
            return len(chunks)

        except Exception as e:
            # Captura y envía una excepción más específica a la capa superior
            raise DocumentProcessingError(
                detail=f"Error ingestando '{file.filename}': {e}"
            )
        finally:
            # Garantiza limpieza del archivo temporal en cualquier caso
            if tmp_file_path and os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)