from fastapi import APIRouter, Query
from services.yandex_api import get_route_info

router = APIRouter()

@router.get("/price")
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
