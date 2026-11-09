from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from pydantic import BaseModel
import asyncio
from services.yandex_api import get_route_info
from services.db import geocode_address

router = APIRouter()

# Сначала определяем модели
class RouteWithName(BaseModel):
    from_lat: float
    from_lon: float
    to_lat: float
    to_lon: float

class GeocodeResponse(BaseModel):
    address_full: str
    street: Optional[str]
    housenumber: Optional[str]
    city: Optional[str]
    longitude: float
    latitude: float

# Потом используем
@router.post("/trip_price_router")
async def get_prices_post(routes: List[RouteWithName]):
    results = await asyncio.gather(*[
        get_route_info(r.from_lon, r.from_lat, r.to_lon, r.to_lat)
        for r in routes
    ])
    return results