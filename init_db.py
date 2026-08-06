
import asyncio
from sentence_transformers import SentenceTransformer
from database import engine, Base, async_session_maker, DocumentModel



model = SentenceTransformer("all-MiniLM-L6-v2")

INITIAL_DOCS = [
    "FastAPI enables high-performance async APIs with automatic Swagger documentation.",
    "OpenTelemetry provides vendor-neutral observability, tracing requests across microservices.",
    "LLM observability requires tracking prompts, tokens, latency, and costs in tools like Jaeger.",
    "PostgreSQL with pgvector allows efficient vector similarity search using cosine distance.",
    "RAG (Retrieval-Augmented Generation) combines vector search with LLMs to ground responses in private data."
]

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    async with async_session_maker() as session:
        for text in INITIAL_DOCS:
            embedding = model.encode(text).tolist()
            new_doc = DocumentModel(content=text, embedding=embedding)
            session.add(new_doc)
            
        await session.commit()
    
    print("DataBase was initialaized successfully")
    
if __name__ == "__main__":
    asyncio.run(async_main())