from fastapi import FastAPI
from routes.get_info import router as base
import uvicorn


app = FastAPI(title="Yandex Taxi Price API")
app.include_router(base, prefix="/api/taxi", tags=["Price"])

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Включаем авто-перезагрузку
        reload_dirs=["."],  # Следить за изменениями в текущей директории
    )





