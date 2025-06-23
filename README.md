# 📄 Konecto QA Microservice

## Descripción del Proyecto
Konecto QA Microservice es un sistema de Preguntas y Respuestas (QA) con RAG (Retrieval‑Augmented Generation). Permite ingestar documentos PDF para crear una base de conocimiento personalizada y luego consultar esa información usando LLMs de OpenAI. Ideal para construir sistemas de soporte o herramientas de investigación basadas en documentos específicos.

## Características
- **Ingesta de PDFs**: Procesamiento de archivos PDF, extracción de texto y generación de embeddings con OpenAI.
- **Base de Datos Vectorial**: Almacenamiento semántico en ChromaDB.
- **Consulta RAG**: Respuestas contextuales basadas en documentos relevantes.
- **Atribución de Fuentes**: Incluye documento, página y fragmento.
- **Gestión de Datos**: Endpoint para limpieza de la base de datos vectorial.
- **API RESTful**: Construida con FastAPI e incluye documentación interactiva (Swagger UI).

## 🗂 Estructura del proyecto

```text
konecto-project/
├── app/
│   ├── api/
│   │   └── routers/
│   │       ├── ingest.py        # Ingreso de PDFs y limpieza de DB
│   │       └── query.py         # Consultas RAG
│   ├── core/
│   │   ├── config.py            # Configuración general
│   │   ├── dependencies.py      # Inyección de dependencias
│   │   └── exceptions.py        # Excepciones personalizadas
│   ├── db/
│   │   └── chroma.py            # Configuración de ChromaDB
│   ├── models/
│   │   └── schemas.py           # Modelos Pydantic para la API
│   └── services/
│       ├── document_service.py  # Procesamiento de PDFs
│       └── qa_service.py        # Lógica RAG
├── .env.example                 # Ejemplo de variables de entorno
├── git-cheat-sheet-education.pdf  # Documento de ejemplo
├── main.py                      # Punto de entrada FastAPI
└── requirements.txt             # Dependencias del proyecto
```

## Requisitos
Python 3.10 o superior (preferiblemente 3.13).

pip.

Acceso a la API de OpenAI (se requiere una API Key).

##Instalación
Clona el repositorio:

git clone `https://github.com/DilanRojasca/konecto-qa-microservice`

cd konecto-project

## crea y activa un entorno virtual:
python -m venv .venv

## macOS/Linux:
source .venv/bin/activate
## Windows (CMD):
.venv\Scripts\activate
## Windows (PowerShell):
.\.venv\Scripts\Activate.ps1

## Instala dependencias:

pip install -r requirements.txt

## Variables de Entorno
Crea un archivo .env en la raíz del proyecto y añade tu clave API de OpenAI:

OPENAI_API_KEY="sk-tu_clave_api_de_openai_aqui"

# Uso
### Iniciar el Microservicio
uvicorn app.main:app --reload

Accede a la API en http://127.0.0.1:8000.

### Acceder a la Documentación de la API
Visita http://127.0.0.1:8000/docs para la documentación interactiva (Swagger UI).

## Endpoints Disponibles
### POST /api/ingest
Descripción: Sube y procesa PDFs.

Parámetros: files (múltiples archivos PDF).

#### Ejemplo curl:

curl -X 'POST' \
  'http://127.0.0.1:8000/api/ingest' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'files=@./path/to/your/document.pdf'

### POST /api/query
Descripción: Consulta documentos ingestados.

Parámetros: query (string).

#### Ejemplo curl:

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

### POST /api/clear_db
Descripción: Elimina todos los documentos de ChromaDB. ¡Advertencia!: Irreversible.

#### Ejemplo curl:

curl -X 'POST' \
  'http://127.0.0.1:8000/api/clear_db' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d ''

