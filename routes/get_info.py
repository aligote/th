from fastapi import APIRouter
from typing import List
from pydantic import BaseModel
import asyncio
from services.yandex_api import get_route_info

router = APIRouter()

class RouteWithName(BaseModel):
    # name_from: str
    # name_to: str
    from_lat: float
    from_lon: float
    to_lat: float
    to_lon: float

@router.post("/trip_price_router")
async def get_prices_post(routes: List[RouteWithName]):
    results = await asyncio.gather(*[
        get_route_info(r.from_lon, r.from_lat, r.to_lon, r.to_lat)
        for r in routes
    ])

    return results