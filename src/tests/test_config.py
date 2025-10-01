import pytest
from src.config import Settings

def test_custom_values():
    settings = Settings(
        app_name="Test",
        openai_api_key="test-key",
        text_completion_model="gpt-3.5-turbo",
        embedding_model="text-embedding-ada-002",
        vector_dimension=256,
        top_k_results=10
    )
    
    assert settings.app_name == "Test"
    assert settings.openai_api_key == "test-key"
    assert settings.text_completion_model == "gpt-3.5-turbo"
    assert settings.embedding_model == "text-embedding-ada-002"
    assert settings.vector_dimension == 256
    assert settings.top_k_results == 10

def test_settings_type_validation():
    settings = Settings(vector_dimension=100, top_k_results=5)
    assert isinstance(settings.vector_dimension, int)
    assert isinstance(settings.top_k_results, int)
    
    assert isinstance(settings.app_name, str)
    assert isinstance(settings.openai_api_key, str)
    assert isinstance(settings.text_completion_model, str)
    assert isinstance(settings.embedding_model, str)