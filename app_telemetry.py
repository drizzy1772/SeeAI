




from fastapi import FastAPI, Request
from opentelemetry import trace
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter
from opentelemetry.trace import Tracer
from opentelemetry.sdk.trace import TracerProvider
from typing import List
import asyncio
import hashlib
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from typing import List
import asyncio
import hashlib

resource = Resource(attributes={
    "service.name": "seeai-rag-telemetry"
})
provider = TracerProvider(resource=resource)

otlp_exporter = OTLPSpanExporter(endpoints="https://127.0.0.1:4317", insecure=True)

processor = BatchSpanProcessor(otlp_exporter)

trace.set_tracer_provider(provider)
tracer: Tracer = trace.get_tracer(__name__)
provider.add_span_processor(processor)


app = FastAPI()

"write all inf in therminal"
provider = TracerProvider()
processor = SimpleSpanProcessor(ConsoleSpanExporter())


trace.set_tracer_provider(provider)
tracer: Tracer = trace.get_tracer(__name__)
provider.add_span_processor(processor)

async def retrieve_documents(query: str) -> List[str]:
    await asyncio.sleep(0.05)
    return [
        "FastAPI enables high-performance async APIs.",
        "OpenTelemetry provides vendor-neutral observability.",
        "LLM observability requires tracing prompts and tokens.",
    ]

def build_promt(query: str, documents: List[str]) -> str:
    save = "\n".join(documents)
    return f"""

Context:
{save}

Question:
{query}

"""

class LLMResponse:
    def __init__(self, text: str, promt_tokens: int, completion_tokens: int):
        self.text = text
        self.promt_tokens = promt_tokens
        self.completion_tokens = completion_tokens
        
    @property
    def total_tokens(self) -> int:
        return self.promt_tokens + self.completion_tokens
        
async def call_llm(promt: str) -> LLMResponse:
    await asyncio.sleep(0.2)
    
    response_text = (
        "FastAPI and OpenTelemetry enable end-to-end LLM observability."
    )
    
    promt_tokens = len(promt.split())
    completion_tokens = len(response_text.split())
    return LLMResponse(response_text, promt_tokens, completion_tokens)

def summarize_response(response: LLMResponse) -> str:
    return response.text

@app.post("/query")
async def raq_query(request: Request, query: str):
    
    with tracer.start_as_current_span("http.request") as http_span:
        http_span.set_attribute("https.method", "POST")
        http_span.set_attribute("https.route", "/query")
    
        with tracer.start_as_current_span("rag.retriveal") as retrieval_span:
            retrieval_span.set_attribute("rag.top_k", 5)
            retrieval_span.set_attribute("rag.similarity_threshold", 0.8)
            documents = await retrieve_documents(query)
            
            retrieval_span.set_attribute(
                "rag/documents_returned",
                len(documents),
            )
            
        with tracer.start_as_current_span("llm.call") as llm_span:
            llm_span.set_attribute("llm.provider", "example")
            llm_span.set_attribute("llm.model", "example-llm")
            llm_span.set_attribute("llm.temperature", 0.7)
            llm_span.set_attribute("llm.promt_template_id", "rag_v1")
            
            promt = build_promt(query, documents)
            
            promt_hash = hashlib.sha256(promt.encode()).hexdigest()
            llm_span.set_attribute("llm.promt_hash", promt_hash)
            llm_span.set_attribute("llm.promt_length", len(promt))
            
            response = await call_llm(promt)
            
            response_hash = hashlib.sha256(
                    response.text.encode()
            ).hexdigest()
            llm_span.set_attribute("llm.response_hash", response_hash)
            
            llm_span.set_attribute("llm.usage.promt_tokens", response.promt_tokens)
            llm_span.set_attribute("llm.usage.completion.tokens", response.completion_tokens)
            llm_span.set_attribute("llm.usage.total_tokens", response.total_tokens)
            
            estimated_cost = response.total_tokens * 0.000002
            llm_span.set_attribute("llm.cost_estimated_usd", estimated_cost)
            
        with tracer.start_as_current_span("llm.postprocess") as post_span:
            summary = summarize_response(response)
            post_span.set_attribute(
                "llm.summary_length",
                len(summary),
            )
    
    return {"summary": summary}