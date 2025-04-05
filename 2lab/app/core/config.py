from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Lab Project"
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    SECRET_KEY: str = "your-secret-key"

    class Config:
        env_file = ".env"

settings = Settings()
