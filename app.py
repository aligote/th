from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes.get_info import router as base
from config import PORT, HOST
import uvicorn
import logging
import sys

# Настройка логирования для всего приложения
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),  # В консоль (для systemd)
       # logging.FileHandler('/var/log/taxi_api/app.log')  # В файл (опционально)
    ]
)

logger = logging.getLogger(__name__)

# Новый современный менеджер жизненного цикла приложения вместо on_event
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Код выполняется при старте (бывший startup)
    logger.info("🚀 API сервис запущен")
    yield
    # Код выполняется при остановке (бывший shutdown)
    logger.info("🛑 API сервис остановлен")

# Передаем lifespan в инициализацию FastAPI
app = FastAPI(title="Yandex Taxi Price API", lifespan=lifespan)

app.include_router(base, prefix="/api/taxi", tags=["Price"])

if __name__ == "__main__":
    logger.info(f"Запуск сервера на {HOST}:{PORT} с {4} воркерами")
    uvicorn.run(
        "app:app",
        host=HOST,
        port=PORT,
        reload=False,
        workers=4,
        log_config=None  # Отключаем логгер uvicorn, используем свой
    )
