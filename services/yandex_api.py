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
    # print('data ------------------------------->', data)
    if not data.get("options"):
        return {"error": "Нет вариантов маршрута"}

    option = data["options"][0]

    price = option["price"]
    time_sec = data["time"]
    distance_m = data["distance"]

    # # Эффективность
    time_min = time_sec / 60
    distance_km = distance_m / 1000

    # rub_per_min = round(price / time_min, 2) if time_min > 0 else 0
    # rub_per_km = round(price / distance_km, 2) if distance_km > 0 else 0

    return {
        "price": price,
        "price_text": option["price_text"],
        "waiting_time_sec": option["waiting_time"],
        "duration_min": round(time_min, 1),
        "distance_km": round(distance_km, 2),
        # "rub_per_min": rub_per_min,
        # "rub_per_km": rub_per_km,
        "class": option["class_name"],
        "class_text": option["class_text"]
    }

