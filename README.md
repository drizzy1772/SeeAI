SeeAI RAG APIA REST API for Retrieval-Augmented Generation (RAG) with semantic vector search, LLM integration, and comprehensive observability built with FastAPI, PostgreSQL (pgvector), Sentence-Transformers, and OpenTelemetry.Tech StackFastAPISQLAlchemy 2.0 (Async)PostgreSQL (pgvector)Sentence-TransformersGroq APIOpenTelemetry & JaegerDocker & Docker ComposeImage IntroductionFeaturesAsynchronous Retrieval-Augmented Generation (RAG) pipelineSemantic vector search using PostgreSQL pgvector and cosine distanceLocal offline embedding generation using all-MiniLM-L6-v2Integration with Groq API for lightning-fast LLM inferenceComprehensive LLM observability (tracking prompts, token usage, latency, and USD cost)Distributed tracing across all operations via OpenTelemetry and JaegerAutomated database initialization and vector indexing scriptPrerequisitesPython 3.10+Docker & Docker ComposeInstallationClone the repositoryBashgit clone https://github.com/your-username/seeai.git
cd seeai
Setup environment variablesBashcp .env.example .env
Edit .env:Фрагмент кодаGROQ_API_KEY=your-groq-api-key-here
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5433/seeai_rag
Start the infrastructure (PostgreSQL & Jaeger)Bashdocker compose up -d
Initialize the database and embeddingsBashpython init_db.py
Run the FastAPI applicationBashuvicorn app_telemetry:app --reload
Swagger UI: http://localhost:8000/docsJaeger UI: http://localhost:16686UsageQuery the RAG SystemBashPOST /query?query=What+is+RAG%3F
Response Example:JSON{
  "summary": "RAG (Retrieval-Augmented Generation) combines vector search with LLMs to ground responses in private data."
}
API SchemeAPI EndpointsAI & RetrievalMethodEndpointAuthPOST/queryNoAPI DocsSwagger UI available at: http://localhost:8000/docsTestingBashpytest
Project StructureSeeAI/
├── app_telemetry.py     # Routes, RAG logic & OpenTelemetry setup
├── database.py          # Async DB connection & DocumentModel
├── init_db.py           # DB initialization & initial embeddings generator
├── docker-compose.yml   # PostgreSQL (pgvector) & Jaeger services
├── .env                 # Environment variables (Groq API, DB URL)
├── .gitignore
├── requirements.txt
└── README.md
Link on API:http://localhost:8000/docsNote: The live deployment is currently configured for local environments. To experience the full observability capabilities via Jaeger and vector search via PostgreSQL, please run the project locally using Docker Compose.AuthorThis project is developed by Drizzy1772.LicenseThis project is licensed under MIT License.
