from pydantic import BaseSettings


class Settings(BaseSettings):
    ENV: str = "develop"
    DEBUG: bool = True

    OPENAI_API_KEY: str

    class Config:
        case_sensitive = True
        env_file = ".env"
