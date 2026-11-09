from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Яндекс АПИ
    YANDEX_CLID: str
    YANDEX_API_KEY: str
    YANDEX_API_URL: str

    # Настройки сервера (FastAPI / Uvicorn)
    PORT: int = 8000
    HOST: str = "0.0.0.0"

    # База данных
    DB_NAME: str
    DB_USER: str
    DB_PASS: str = ""  # Если пароль пустой, будет пустая строка
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432

    # Конфиг для чтения .env файла
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8"
    )

# Экземпляр для импорта в другие файлы
settings = Settings()

