from pydantic import BaseModel, Field
from typing import Optional, List
# Esquema para la respuesta del endpoint de ingesta
class IngestResponse(BaseModel):
    """
    Esquema para la respuesta de la ingesta de documentos.
    Indica el número total de fragmentos de documentos procesados.
    """
    # Pydantic 2 infiere que 'ingested_documents' es requerido si no tiene un default.
    # No usamos Field aquí, solo el tipo.
    ingested_documents: int = Field(
        default=...,#"..." indica que el valor del campo requerido no está predefinido
        description="Numero total de chunks de documentos PDF ingestados.",
    )

# Esquema para la solicitud del endpoint de consulta
class QueryRequest(BaseModel):
    """
    Esquema para la solicitud de consulta.
    Espera una cadena de texto que representa la pregunta del usuario.
    """
    # Pydantic 2 infiere que 'query' es requerido.
    # Nota: Aquí perdemos min_length y example del Field anterior.
    query: str = Field(
        default=...,
        min_length=1,
        examples=["Cual es el proceso para ingest documentos"],
        description="El texto que representa el usuario."
    )
class Source(BaseModel):
    """
    Representa una fuente de información de un documento recuperado.
    """
    document: str = Field(
        ...,
        examples=["git-cheat-sheet-education.pdf"], # Actualizado a examples
        description="Nombre del documento original de donde se obtuvo la información."
    )
    page: Optional[int] = Field(
        None,
        examples=[12], # Actualizado a examples
        description="Número de página del documento donde se encontró la información."
    )
    snippet: str = Field(
        ...,
        examples=["relevant text snippet..."], # Actualizado a examples
        description="Fragmento de texto relevante extraído del documento."
    )

# Esquema para la respuesta del endpoint de consulta (ahora incluye fuentes)
class QueryResponse(BaseModel):
    """
    Esquema para la respuesta de una consulta.
    Contiene la respuesta generada por el LLM y las fuentes utilizadas.
    """
    # *** CORRECCIÓN AQUÍ ***: Cambiar 'response' a 'answer'
    answer: str = Field(
        default=...,
        examples=["Según los documentos, el proceso de ingesta implica..."], # Actualizado a examples
        description="La respuesta generada por el modelo a la pregunta del usuario."
    )
    sources: List[Source] = Field(
        default_factory=list,
        description="Lista de documentos fuente utilizados para generar la respuesta, incluyendo fragmentos relevantes."
    )