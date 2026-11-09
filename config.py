from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Яндекс АПИ
    YANDEX_CLID: str
    YANDEX_API_KEY: str
    YANDEX_API_URL: str

    # Настройки сервера
    PORT: int = 8000
    HOST: str = "0.0.0.0"

    # База данных
    DB_NAME: str
    DB_USER: str
    DB_PASS: str = ""
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8"
    )

# 1. Создаем скрытый экземпляр настроек
_settings = Settings()

# 2. Вытаскиваем переменные наружу, чтобы их можно было импортировать напрямую
YANDEX_CLID = _settings.YANDEX_CLID
YANDEX_API_KEY = _settings.YANDEX_API_KEY
YANDEX_API_URL = _settings.YANDEX_API_URL

PORT = _settings.PORT
HOST = _settings.HOST

DB_NAME = _settings.DB_NAME
DB_USER = _settings.DB_USER
DB_PASS = _settings.DB_PASS
DB_HOST = _settings.DB_HOST
DB_PORT = _settings.DB_PORT

