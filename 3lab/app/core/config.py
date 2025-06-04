from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Lab Project"
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    SECRET_KEY: str  # Не указываем значение по умолчанию, оно будет загружаться из .env

    class Config:
        env_file = ".env"  # Указываем, что настройки будут загружаться из файла .env

# Создаем объект settings для доступа к значениям
settings = Settings()
