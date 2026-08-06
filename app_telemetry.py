




from fastapi import FastAPI, Request
from opentelemetry import trace
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter
from opentelemetry.trace import Tracer
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource

from typing import List
import asyncio
import hashlib
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from typing import List
import asyncio
import hashlib

import os
import hashlib
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

client = AsyncOpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)


resource = Resource(attributes={
    "service.name": "seeai-rag-telemetry"
})
provider = TracerProvider(resource=resource)

otlp_exporter = OTLPSpanExporter(endpoint="127.0.0.1:4317", insecure=True)

processor = BatchSpanProcessor(otlp_exporter)

trace.set_tracer_provider(provider)
tracer: Tracer = trace.get_tracer(__name__)
provider.add_span_processor(processor)


app = FastAPI()

async def retrieve_documents(query: str) -> List[str]:
    await asyncio.sleep(0.05)
    return [
        "FastAPI enables high-performance async APIs.",
        "OpenTelemetry provides vendor-neutral observability.",
        "LLM observability requires tracing prompts and tokens.",
    ]

def build_promt(query: str, documents: List[str]) -> str:
    save = "\n".join(documents)
    return f"Context:\n{save}\n\nQuestion:\n{query}"


@tracer.start_as_current_span("llm_call")
async def call_llm(promt: str) -> str:
    span = trace.get_current_span()
    
    promt_hash = hashlib.sha256(promt.encode('utf-8')).hexdigest()
    span.set_attribute("llm.request.promt_hash", promt_hash)
    
    model_name = "openai/gpt-oss-20b"
    span.set_attribute("llm.model", model_name)
    span.set_attribute("llm.provider", "groq")
    
    try:
        response = await client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant. Answer concisely."},
                {"role": "user", "content": promt}
            ],
            temperature=0.7,
        )

        answer = response.choices[0].message.content
        
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens
        total_tokens = response.usage.total_tokens
        
        span.set_attribute("llm.usage.promt_tokens", prompt_tokens)
        span.set_attribute("llm.usage.completion_tokens", completion_tokens)
        span.set_attribute("llm.usage.total_tokens", total_tokens)
        
        cost = (total_tokens / 1_000_000) * 0.05
        span.set_attribute("llm.cost.usd", cost)
        
        response_hash = hashlib.sha256(answer.encode('utf-8')).hexdigest()
        span.set_attribute("llm.response.hash", response_hash)
        return answer
    
    except Exception as e:
        span.record_exception(e)
        span.set_status(trace.status.Status(trace.status.StatusCode.ERROR))
        raise e


@app.post("/query")
async def raq_query(request: Request, query: str):
    
    with tracer.start_as_current_span("http.request") as http_span:
        http_span.set_attribute("https.method", "POST")
        http_span.set_attribute("https.route", "/query")
    
        with tracer.start_as_current_span("rag.retriveal") as retrieval_span:
            retrieval_span.set_attribute("rag.top_k", 3)
            documents = await retrieve_documents(query)
            retrieval_span.set_attribute("rag.similarity_threshold", len(documents))
            
        promt = build_promt(query, documents)    
        
        answer = await call_llm(promt)
        
        with tracer.start_as_current_span("llm.postprocess") as post_span:
            post_span.set_attribute(
                "llm.summary_length",
                len(answer),
            )
    
    return {"summary": answer}