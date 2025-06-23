📄 Konecto QA Microservice
Descripción del Proyecto
Konecto QA Microservice es un sistema de Preguntas y Respuestas (QA) con RAG (Retrieval-Augmented Generation). Permite ingestar documentos PDF para crear una base de conocimiento personalizada y luego consultar esta información usando LLMs de OpenAI. Ideal para construir sistemas de soporte o herramientas de investigación basadas en documentos específicos.

Características
Ingesta de PDFs: Procesa archivos PDF, extrayendo texto y generando embeddings con OpenAI.

Base de Datos Vectorial: Almacena embeddings en ChromaDB para una búsqueda semántica eficiente.

Consulta RAG: Genera respuestas contextuales utilizando LLMs de OpenAI, basándose en los documentos relevantes recuperados.

Atribución de Fuentes: Muestra el documento, página y fragmento de texto de donde se extrajo la información.

Gestión de Datos: Endpoint para limpiar la base de datos vectorial de ChromaDB.

API RESTful: Construido con FastAPI, incluye documentación interactiva (Swagger UI).

Estructura del Proyecto
El proyecto sigue una estructura modular para facilitar la organización y el mantenimiento:

konecto-project/
├── app/
│   ├── api/
│   │   └── routers/
│   │       ├── ingest.py       # Ingreso de PDFs y limpieza de DB.
│   │       └── query.py        # Consultas RAG.
│   ├── core/
│   │   ├── config.py           # Configuración.
│   │   ├── dependencies.py     # Inyección de dependencias.
│   │   └── exceptions.py       # Excepciones personalizadas.
│   ├── db/
│   │   └── chroma.py           # Configuración y limpieza de ChromaDB.
│   ├── models/
│   │   └── schemas.py          # Modelos Pydantic para API.
│   └── services/
│       ├── document_service.py # Procesamiento de PDFs.
│       └── qa_service.py       # Lógica RAG.
├── .env.example                # Ejemplo de variables de entorno.
├── git-cheat-sheet-education.pdf # Ejemplo de documento.
├── main.py                     # Punto de entrada de FastAPI.
└── requirements.txt            # Dependencias.

Requisitos
Python 3.10 o superior (preferiblemente 3.13).

pip.

Acceso a la API de OpenAI (se requiere una API Key).

Instalación
Clona el repositorio:

git clone <URL_DE_TU_REPOSITORIO>
cd konecto-project

Crea y activa un entorno virtual:

python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows (CMD):
.venv\Scripts\activate
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1

Instala dependencias:

pip install -r requirements.txt

Variables de Entorno
Crea un archivo .env en la raíz del proyecto y añade tu clave API de OpenAI:

OPENAI_API_KEY="sk-tu_clave_api_de_openai_aqui"

Uso
Iniciar el Microservicio
uvicorn app.main:app --reload

Accede a la API en http://127.0.0.1:8000.

Acceder a la Documentación de la API
Visita http://127.0.0.1:8000/docs para la documentación interactiva (Swagger UI).

Endpoints Disponibles
POST /api/ingest
Descripción: Sube y procesa PDFs.

Parámetros: files (múltiples archivos PDF).

Ejemplo curl:

curl -X 'POST' \
  'http://127.0.0.1:8000/api/ingest' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'files=@./path/to/your/document.pdf'

POST /api/query
Descripción: Consulta documentos ingestados.

Parámetros: query (string).

Ejemplo curl:

curl -X 'POST' \
  'http://127.0.0.1:8000/api/query' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "¿Qué es Git Status y para qué se utiliza?"
}'

Respuesta esperada:

{
  "answer": "...",
  "sources": [
    {
      "document": "nombre_del_archivo.pdf",
      "page": 1,
      "snippet": "fragmento de texto relevante..."
    }
  ]
}

POST /api/clear_db
Descripción: Elimina todos los documentos de ChromaDB. ¡Advertencia!: Irreversible.

Ejemplo curl:

curl -X 'POST' \
  'http://127.0.0.1:8000/api/clear_db' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d ''

Contribución
Haz un "fork" del repositorio.

Crea una nueva rama (git checkout -b feature/tu-funcionalidad).

Haz tus commits (git commit -m "feat: nueva funcionalidad").

Envía tus cambios (git push origin feature/tu-funcionalidad).

Abre un Pull Request.

Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.