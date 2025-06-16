from fastapi import APIRouter, Query
from typing import List
from pydantic import BaseModel
import asyncio
from services.yandex_api import get_route_info

router = APIRouter()


class RouteWithName(BaseModel):
    name_from: str
    name_to: str
    from_lat: float
    from_lon: float
    to_lat: float
    to_lon: float

async def get_route_info_extended(from_lat, from_lon, to_lat, to_lon):
    # Здесь вызываешь свой get_route_info, 
    # предположим, он возвращает словарь с ценой, временем, расстоянием, etc.
    # Пример возвращаемых данных:
    # {
    #   "price": 212,
    #   "duration": 10,      # в минутах
    #   "distance": 4,       # в километрах
    #   "price_per_min": 22,
    #   "price_per_km": 52
    # }
    return await get_route_info(from_lat, from_lon, to_lat, to_lon)

def calculate_efficiency(price_per_min, price_per_km):
    # Пример: среднее значение коэффициента из двух показателей
    # Можно адаптировать под свою логику
    max_price_per_min = 50  # пример максимума для нормализации
    max_price_per_km = 100
    norm_min = price_per_min / max_price_per_min
    norm_km = price_per_km / max_price_per_km
    coeff = (norm_min + norm_km) / 2  # усреднённый коэффициент (0..1)
    return round(coeff * 100, 1)  # в процентах

@router.post("/trip_price_router")
async def get_prices_post(routes: List[RouteWithName]):
    results = await asyncio.gather(*[
        get_route_info_extended(r.from_lat, r.from_lon, r.to_lat, r.to_lon)
        for r in routes
    ])

    response = []
    for r, info in zip(routes, results):
        coeff = calculate_efficiency(info["price_per_min"], info["price_per_km"])
        response.append({
            "route": f'{r.name_from} - {r.name_to}',
            "price": info["price"],
            "duration_min": info["duration"],
            "distance_km": info["distance"],
            "price_per_min": info["price_per_min"],
            "price_per_km": info["price_per_km"],
            "efficiency_coeff_percent": coeff
        })
    return response