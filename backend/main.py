from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI
import wandb
import os
import time
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()
app = FastAPI()

# CORS for frontend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize W&B
wandb.init(project="rag-demo", name="inference-tracking", reinit=True)

# Azure Search Configuration
SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
SEARCH_INDEX = os.getenv("AZURE_SEARCH_INDEX")

search_client = SearchClient(
    endpoint=SEARCH_ENDPOINT,
    index_name=SEARCH_INDEX,
    credential=AzureKeyCredential(SEARCH_KEY)
)

# Azure OpenAI Configuration
DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT")
openai_client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2023-05-15",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

class QueryRequest(BaseModel):
    query: str

class FeedbackRequest(BaseModel):
    query: str
    feedback: str

def retrieve_documents(query: str) -> List[dict]:
    results = search_client.search(
        search_text=query,
        top=3,
        query_type="semantic",
        semantic_configuration_name="default"
    )
    return [doc for doc in results]

def generate_answer(query: str, context_docs: List[str]) -> str:
    context_text = "\n".join(context_docs)
    prompt = f"""
    You are an assistant. Use the following context to answer the question.

    Context:
    {context_text}

    Question:
    {query}
    """
    response = openai_client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

@app.post("/api/query")
async def query_handler(req: QueryRequest):
    start = time.time()
    docs = retrieve_documents(req.query)
    context = [doc["content"] for doc in docs]
    answer = generate_answer(req.query, context)

    wandb.log({
        "query": req.query,
        "retrieved_doc_ids": [doc["id"] for doc in docs],
        "retrieved_text": context,
        "generated_answer": answer,
        "latency_ms": round((time.time() - start) * 1000, 2)
    })

    return {
        "answer": answer,
        "sources": context
    }

@app.post("/api/feedback")
async def feedback_handler(req: FeedbackRequest):
    feedback_type = "positive" if req.feedback == "👍" else "negative"
    wandb.log({
        "feedback_query": req.query,
        "user_feedback": req.feedback,
        "feedback_type": feedback_type
    })
    return {"status": "feedback recorded"}

