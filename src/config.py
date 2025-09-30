from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name : str = "Knowledge Assistant for Support Team"
    openai_api_key : str = ""
    text_completion_model : str = "gpt-4o"
    embedding_model : str = "text-embedding-3-small"
    vector_dimension : int = 512
    top_k_results : int = 5

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        assert self.vector_dimension > 0, "vector_dimension must be positive"
        assert self.top_k_results > 0, "top_k_results must be positive"


settings = Settings(_env_file=".env")

