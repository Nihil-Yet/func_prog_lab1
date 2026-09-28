import logging
from dataclasses import dataclass

import requests

from env_manager import GEO_API_FALLBACK_CITY, GEO_API_URL

log = logging.getLogger(__name__)


@dataclass
class Location:
    city: str
    lat: float | None = None
    lon: float | None = None


def get_location() -> Location:
    if GEO_API_URL:
        try:
            r = requests.get(GEO_API_URL, timeout=5)
            r.raise_for_status()
            data = r.json()
            city = data.get("city")

            lat = data.get("lat")
            lon = data.get("lon")
            if lat is None:
                lat = data.get("latitude")
            if lon is None:
                lon = data.get("longitude")

            if city and lat is not None and lon is not None:
                log.info("Локация по IP: %s (%.4f, %.4f)", city, lat, lon)
                return Location(city, float(lat), float(lon))
            log.warning("В ответе %s нет city/latitude/longitude", GEO_API_URL)
        except requests.RequestException as e:
            log.warning("Запрос к %s провалился: %s", GEO_API_URL, e)
        except ValueError as e:
            log.warning("Не удалось распарсить JSON от %s: %s", GEO_API_URL, e)
    else:
        log.warning("GEO_API_URL не задан")

    if GEO_API_FALLBACK_CITY:
        return Location(GEO_API_FALLBACK_CITY)

    log.critical("GEO_API_FALLBACK_CITY и GEO_API_URL отсутствуют")
    raise RuntimeError(
        "Не удалось определить город. Задайте рабочий GEO_API_URL "
        "или GEO_API_FALLBACK_CITY в .env."
    )
