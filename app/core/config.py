import os
from dotenv import load_dotenv

# Carga variables de entorno desde el archivo .env para configuraciones sensibles.
load_dotenv()

class Settings:
    """Clase para gestionar la configuración de la aplicación."""
    # Obtiene la clave de API de OpenAI de las variables de entorno.
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")

    # Valida que la clave de API esté configurada; lanza un error si no lo está.
    if OPENAI_API_KEY is None:
        raise ValueError("La variable de entorno OPENAI_API_KEY no está configurada.")

# Instancia global de la configuración para acceso consistente.
settings = Settings()

# Define la ruta del directorio para la persistencia de la base de datos Chroma.
CHROMA_DB_PATH = "./chroma_db"