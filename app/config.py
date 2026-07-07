from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@db:5432/support_db"
    groq_api_key: str = ""
    chroma_persist_dir: str = "./chroma_db"
    similarity_threshold: float = 0.35   # tune this after testing — below this, respond "I don't know"
    top_k_chunks: int = 4
    chunk_size: int = 500
    chunk_overlap: int = 50
    log_level: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()