from fastapi import HTTPException
from .llm import OpenAIClient, PROMPT_TEMPLATE
from .embeddings import Encoder, VectorStore
from .data import get_sample_documents
import json

encoder = Encoder()
vector_store = VectorStore()
openai_client = OpenAIClient()

def initialize_data():
    documents = get_sample_documents()
    text = [doc["content"] for doc in documents]
    embeddings = encoder.get_encoding(text)
    vector_store.add_documents(documents, embeddings)

def resolve_ticket(request_data):

    try:
        ticket_text = request_data.get("ticket_text", "")

        if not ticket_text:
            raise HTTPException(status_code=400, detail="ticket_text is required")
        
        query_embedding = encoder.get_encoding([ticket_text])[0]
        search_results = vector_store.search(query_embedding)

        context_docs = []
        for document, score in search_results:
            context_docs.append({
                "source": document.get("source", "Unknown"),
                "section": document.get("section", "N/A"),
                "content": document.get("content", ""),
                "score": score
            })
        
        context_text = ""
        if context_docs:
            context_text = "\n\n".join([
                f"Document: {doc['source']}\n"
                f"Section: {doc['section']}\n"
                f"Content: {doc['content']}"
                for doc in context_docs
            ])
        
        prompt = PROMPT_TEMPLATE.format(
            context_text=context_text,
            query=ticket_text
        )
        llm_response = openai_client.generate_response(prompt)

        try:
            response_data = json.loads(llm_response)
            return {
                "answer": response_data.get("answer", "Unable to process your request."),
                "references": response_data.get("references", []),
                "action_required": response_data.get("action_required", "technical_escalation")
            }
        except json.JSONDecodeError:
            return {
                "answer": llm_response,
                "references": [],
                "action_required": "technical_escalation"
            }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing ticket: {str(e)}")

def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "0.1.0"
    }

def root():
    """Root endpoint"""
    return {"message": "AI Knowledge Assistant API", "version": "0.1.0"}
