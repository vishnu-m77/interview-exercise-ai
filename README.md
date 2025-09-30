# AI Knowledge Assistant for Support Team

A minimal LLM-powered RAG system that helps a support team respond to customer tickets efficiently using relevant documentation.

## Installation
1. Create a virtual environment:
```bash
python3 -m venv .
source bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up OpenAI API key:
```bash
export OPENAI_API_KEY="your_openai_api_key_here"
```

Or create a `.env` file:
```bash
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
```

## Running the Application

Start the server:
```bash
uvicorn src.main:app --reload --host localhost --port 8000
```

The application will automatically initialize the vector store with sample data on startup.

## API Usage

### Health Check
```bash
curl http://localhost:8000/health
```

### Resolve Support Ticket
```bash
curl -X POST "http://localhost:8000/resolve-ticket" \
     -H "Content-Type: application/json" \
     -d '"My domain was suspended"'
```

Response format:
```json
{
  "answer": "Detailed response based on documentation",
  "references": ["Source: Document Title, Section X.Y"],
  "action_required": "escalate_to_abuse_team|escalate_to_billing_team|escalate_to_legal_team|escalate_to_operations_team|resolved"
}
```

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /resolve-ticket` - Resolve support ticket (expects ticket_text as JSON string)

## Testing

Run tests:
```bash
pytest src/tests/
```

## Project Structure

```
src/
- main.py          # FastAPI application
- config.py        # Configuration settings
- api.py           # API logic and endpoints
- llm.py           # OpenAI client and prompts
- embeddings.py    # Embedding encoder and vector store
- data.py          # Sample domain registrar documents
- tests/           # Test files
```

## Configuration
The application uses the following default settings which can be modified in `src/config.py`:

- `openai_api_key`: Required OpenAI API key
- `text_completion_model`: "gpt-4o"
- `embedding_model`: "text-embedding-3-small"
- `vector_dimension`: 512
- `top_k_results`: 5

## Improvements

- Implementing guardrails to ensure that the model does not hallucinate or provide responses outside the scope of the input data.
- Setting up an evaluation loop that wraps the model which will enable to model to learn from its responses and expected behaviour.
