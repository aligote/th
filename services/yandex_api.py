import httpx
import logging
from config import YANDEX_API_URL, YANDEX_API_KEY, YANDEX_CLID
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
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

    logger.info(f"Запрос к Яндекс API: {lon_from},{lat_from} -> {lon_to},{lat_to}")
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(YANDEX_API_URL, params=params)
        
        logger.info(f"Ответ от Яндекс API: статус {response.status_code}")
        
        if response.status_code != 200:
            logger.error(f"Яндекс API ошибка {response.status_code}: {response.text[:200]}")
            return {
                "error": response.text,
                "status": response.status_code
            }

        data = response.json()
        
        if not data.get("options"):
            logger.warning(f"Нет вариантов маршрута для {lon_from},{lat_from} -> {lon_to},{lat_to}")
            return {"error": "Нет вариантов маршрута"}

        options_count = len(data.get("options", []))
        logger.info(f"Получено {options_count} вариантов маршрута")
        
        return data
        
    except httpx.TimeoutException:
        logger.error(f"Таймаут при запросе к Яндекс API")
        return {"error": "Таймаут при запросе к Яндекс API"}
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {str(e)}", exc_info=True)
        return {"error": f"Внутренняя ошибка: {str(e)}"}