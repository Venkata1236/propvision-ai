from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Centralized application configuration.
    Loads all environment variables from .env.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # =========================
    # APP CONFIG
    # =========================
    app_name: str = Field(default="PropVision AI")
    app_version: str = Field(default="1.0.0")
    debug: bool = Field(default=True)

    # =========================
    # API CONFIG
    # =========================
    api_v1_prefix: str = Field(default="/api/v1")

    # =========================
    # OPENAI
    # =========================
    openai_api_key: str

    # =========================
    # OPENAI MODEL CONFIG
    # =========================
    openai_model: str = Field(default="gpt-3.5-turbo")
    
    openai_embedding_model: str = Field(
        default="text-embedding-ada-002"
    )

    # =========================
    # LANGSMITH
    # =========================
    langchain_api_key: str
    langchain_tracing_v2: bool = Field(default=True)
    langchain_project: str = Field(default="propvision-ai")

    # =========================
    # DATABASE
    # =========================
    database_url: str

    # =========================
    # MODEL PATHS
    # =========================
    xgb_model_path: str
    lgbm_model_path: str
    meta_model_path: str
    preprocessor_path: str
    feature_names_path: str

    # =========================
    # SHAP
    # =========================
    shap_explainer_path: str

    # =========================
    # FAISS
    # =========================
    faiss_index_path: str
    faiss_metadata_path: str

    # =========================
    # RETRIEVAL
    # =========================
    top_k_comparables: int = Field(default=3)

    # =========================
    # CONFIDENCE INTERVAL
    # =========================
    confidence_z_score: float = Field(default=1.96)

    # =========================
    # LOGGING
    # =========================
    log_level: str = Field(default="INFO")


@lru_cache
def get_settings() -> Settings:
    """
    Cached settings instance.
    Prevents reloading env variables repeatedly.
    """
    return Settings()


settings = get_settings()