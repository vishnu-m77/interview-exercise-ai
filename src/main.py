from fastapi import FastAPI, Body
from .config import settings
from .api import resolve_ticket, health_check, root, initialize_data

def initialize_vector_store():
    try:
        initialize_data()
    except Exception as e:
        print(f"Could not initialize vector store: {e}")
        raise

initialize_vector_store()

app = FastAPI(
    title = settings.app_name,
    description = "a minimal LLM-powered RAG system that helps a support team respond to customer tickets efficiently using relevant documentation",
    version = "0.1.0"
)

@app.post("/resolve-ticket")
def resolve_ticket_endpoint(ticket_text: str = Body(...)):
    return resolve_ticket({"ticket_text": ticket_text})

@app.get("/health")
def health_endpoint():
    return health_check()

@app.get("/")
def root_endpoint():
    return root()
