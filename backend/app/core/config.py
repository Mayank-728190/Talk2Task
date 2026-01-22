from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    LIVEKIT_API_KEY: str
    LIVEKIT_API_SECRET: str
    LIVEKIT_URL: str
    FRONTEND_URL: str = "http://localhost:3000"

    DEEPGRAM_API_KEY: str | None = None
    OPENAI_API_KEY: str
    GEMINI_API_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow",
    )

settings = Settings()
