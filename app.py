from fastapi import FastAPI
from routes.get_info import router as base


app = FastAPI(title="Yandex Taxi Price API")
app.include_router(base, prefix="/api/taxi", tags=["Price"])





