from fastapi import APIRouter, Query
from typing import List
from pydantic import BaseModel
import asyncio
from services.yandex_api import get_route_info

router = APIRouter()

@router.get("/trip_price_router")
async def get_price_estimate(
    #44.926696, 37.321312 Россиянка   до 44.881016, 37.336812 Красная площадь
    # from_lat: float = 44.926696,                           #Query(...),
    # from_lon: float = 37.321312,                      #Query(...),

    # to_lat: float =   44.881016,
    #                                                     #Query(...),
    # to_lon: float =   37.336812
                                                #Query(...),
    #service_class: str = Query("econom")
    # request with validations Query - lib from fastapi
    from_lat: float = Query(..., description="Широта точки отправления"),
    from_lon: float = Query(..., description="Долгота точки отправления"),
    to_lat: float = Query(..., description="Широта точки назначения"),
    to_lon: float = Query(..., description="Долгота точки назначения"),
    # service_class: str = Query("econom", description="Класс поездки")
        ):
    return await get_route_info(from_lat, from_lon, to_lat, to_lon)



# Модель для одного маршрута
class Route(BaseModel):
    from_lat: float
    from_lon: float
    to_lat: float
    to_lon: float

# Общая функция для параллельного вызова
async def fetch_prices(routes: List[Route]):
    tasks = [get_route_info(r.from_lat, r.from_lon, r.to_lat, r.to_lon) for r in routes]
    return await asyncio.gather(*tasks)

# Новый POST-роутер для списка маршрутов
@router.post("/trip_price_router")
async def get_prices_post(routes: List[Route]):
    return await fetch_prices(routes)

