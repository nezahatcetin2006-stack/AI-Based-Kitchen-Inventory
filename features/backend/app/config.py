from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8",extra="ignore")

    PORT: int = 8000
    DATABASE_URL: str = "postgresql+psycopg2://inventory:inventory@localhost:5432/kitchen_inventory"
    CORS_ORIGINS: str = "http://localhost:3000"
    SEED_DEMO: bool = True
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.2-11b-vision-preview"
    VISION_MAX_IMAGE_BYTES: int = 4194304

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]


settings = Settings()

