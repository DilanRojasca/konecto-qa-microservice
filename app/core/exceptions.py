# app/core/exceptions.py

from fastapi import HTTPException, status

class APIError(HTTPException):
    """
    Excepción base para errores específicos de la API.
    Permite definir un código de estado HTTP y un mensaje de detalle.
    """
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

class DocumentProcessingError(APIError):
    """
    Excepción específica para errores ocurridos durante el procesamiento de documentos (ingesta).
    """
    def __init__(self, detail: str = "Error al procesar el documento."):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

class QueryProcessingError(APIError):
    """
    Excepción específica para errores ocurridos durante el procesamiento de consultas RAG.
    """
    def __init__(self, detail: str = "Error al procesar la consulta."):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

class InvalidFileTypeError(APIError):
    """
    Excepción para cuando se sube un tipo de archivo no permitido.
    """
    def __init__(self, filename: str = "archivo", allowed_types: str = ".pdf"):
        detail = f"El archivo '{filename}' no es un tipo permitido. Solo se aceptan archivos {allowed_types}."
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)