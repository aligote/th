import httpx
from config import YANDEX_API_URL, YANDEX_API_KEY, YANDEX_CLID

async def get_route_info(
    lon_from: float,
    lat_from: float,
    lon_to: float,
    lat_to: float,
    service_class: str = "econom"
) -> dict:
    params = {
        "clid": YANDEX_CLID,
        "apikey": YANDEX_API_KEY,
        "rll": f"{lon_from},{lat_from}~{lon_to},{lat_to}",
        "class": service_class,
        "req": "calc_ko"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(YANDEX_API_URL, params=params)

    if response.status_code != 200:
        return {
            "error": response.text,
            "status": response.status_code
        }

    data = response.json()
    
    if not data.get("options"):
        return {"error": "Нет вариантов маршрута"}

    return data
    