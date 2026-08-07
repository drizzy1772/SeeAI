
# SeeAI

A REST API for Retrieval-Augmented Generation (RAG) with semantic vector search, LLM integration, and comprehensive observability built with FastAPI, PostgreSQL (pgvector), Sentence-Transformers, and OpenTelemetry.

## Tech Stack

- **FastAPI**
- **SQLAlchemy 2.0 (Async)**
- **PostgreSQL (pgvector)**
- **Sentence-Transformers**
- **Groq/ Groq API**
- **OpenTelemetry & Jaeger**
- **Docker & Docker Compose**

## Features

* Asynchronous Retrieval-Augmented Generation (RAG) pipeline

* Semantic vector search using PostgreSQL pgvector and cosine distance

* Local offline embedding generation using all-MiniLM-L6-v2

* Integration with Groq API for lightning-fast LLM inference

* Comprehensive LLM observability (tracking prompts, token usage, latency, and USD cost)

* Distributed tracing across all operations via OpenTelemetry and Jaeger

* Automated database initialization and vector indexing script

## Prerequisites

* Python 3.10+
* Docker & Docker Compose

1. **Clone the repository**
```bash
git clone https://github.com/your-username/seeai.git
cd seeai
```

2. **Setup environment variables**
```bash
cp .env.example .env
```


3. Edit `.env`:
```env
GROQ_API_KEY=your-groq-api-key-here
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5433/seeai_rag
```
4. **Start the infrastructure (PostgreSQL & Jaeger)**
```bash
docker compose up -d
```

5. **Initialize the database and embeddings**
```bash
python init_db.py
```

6. **Run the FastAPI application**
```bash
uvicorn app_telemetry:app --reload
```

- **Swagger UI**: http://localhost:8080/docs
- **Jaeger UI**: http://localhost:16686

## Usage
```bash
POST /query?query=What+is+RAG%3F
```

## Response Example
{
  "summary": "RAG (Retrieval-Augmented Generation)
  combines vector search with LLMs to ground responses in private data."
}

## API ENDPOINTS

| Method | Endpoint | Auth |
|--------|----------|------|
| POST | `/query` | No |

## API Docs
Swagger UI available at: http://localhost:8000/docs

## Testing
## Project Structure

```text
SeeAI/

├──.github/workflows
│   ├── evals.yml                    # CI/CD yml.
├── agent_evals/                     # LLM Agent evaluation framework
│   ├── evaluators.py                # Logic for evaluating agent responses
│   ├── experiment.py                # Experiment tracking and execution
│   ├── generator.py                 # Test data and prompt generators
│   ├── models.py                    # Data schemas for evaluations
│   ├── pytest_utils.py              # Utilities for pytest integration
│   └── __init__.py
├── app_telemetry.py                 # FastAPI routes, RAG logic & OpenTelemetry setup
├── database.py                      # Async DB connection & DocumentModel schema
├── init_db.py                       # DB init script & embeddings generator
├── docker-compose.yml               # PostgreSQL (pgvector) & Jaeger services
├── requirements.txt                 # Project dependencies
├── .env                             # Environment variables (Groq API, DB URL)
├── .gitignore                       # Git ignored files and folders
├── README.md                        # Project documentation
│
└── Tests/                           # Pytest suite
    ├── test_async.py                # Tests for async operations
    ├── test_deterministic_evaluators.py 
    ├── test_evals.py                # Core evaluation pipeline tests
    ├── test_generator.py            # Tests for generation logic
    ├── test_hyperparams.py          # Hyperparameter tuning tests
    ├── test_output_evaluator.py     # LLM output evaluation tests
    ├── test_run.py                  # App execution tests
    ├── test_trajectory.py           # Agent interaction trajectory tests
    └── test_trajectory_evaluator.py # Trajectory evaluation tests
```


## Author

This project is developed by Drizzy1772.

## License

This project is licensed under MIT License.







