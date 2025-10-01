import pytest
import openai
from src.llm import OpenAIClient, PROMPT_TEMPLATE
from src.config import settings

def test_init():
    client = OpenAIClient()
    assert client.model == settings.text_completion_model
    assert client.client is not None
    assert isinstance(client.client, openai.OpenAI)


def test_prompt_template_format():
    context = "Test context"
    query = "Test query"
    
    prompt = PROMPT_TEMPLATE.format(context_text = context, query = query)
    
    assert context in prompt
    assert query in prompt
    assert "Context Documents:" in prompt
    assert "Customer Query:" in prompt
    assert "resolved" in prompt
    assert "escalate_to_abuse_team" in prompt

def test_prompt_template_structure():
    context = "Sample context"
    query = "Sample query"
    
    prompt = PROMPT_TEMPLATE.format(context_text = context, query = query)
    
    assert '"answer"' in prompt
    assert '"references"' in prompt
    assert '"action_required"' in prompt
    
    assert "escalate_to_abuse_team" in prompt
    assert "escalate_to_billing_team" in prompt
    assert "escalate_to_legal_team" in prompt
    assert "escalate_to_operations_team" in prompt
    assert "resolved" in prompt