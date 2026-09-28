from collections import defaultdict
from datetime import date, datetime, timezone

import requests

from env_manager import WEATHER_API_KEY, WEATHER_API_URL, log
from geoloc import Location


def fetch_forecast(loc: Location) -> list[dict]:
    params: dict[str, str | float] = {
        "appid": WEATHER_API_KEY,
        "units": "metric",
        "lang": "ru",
    }

    if loc.lat is not None and loc.lon is not None:
        params["lat"] = loc.lat
        params["lon"] = loc.lon
        log.info("Прогноз по координатам: %s (%.4f, %.4f)", loc.city, loc.lat, loc.lon)
    else:
        params["q"] = loc.city
        log.info("Прогноз по имени города: %s", loc.city)

    r = requests.get(f"{WEATHER_API_URL}/forecast", params=params, timeout=10)
    r.raise_for_status()
    return r.json()["list"]


def aggregate_daily(items: list[dict], days: int = 4) -> list[dict]:
    by_day: dict[date, list[dict]] = defaultdict(list)
    for item in items:
        d = datetime.fromisoformat(item["dt_txt"]).date()
        by_day[d].append(item)

    today = datetime.now(tz=timezone.utc).date()
    result = []
    for d in sorted(by_day):
        if d < today:
            continue
        if len(result) >= days:
            break

        entries = by_day[d]
        temps_min = [e["main"]["temp_min"] for e in entries]
        temps_max = [e["main"]["temp_max"] for e in entries]
        humidity = [e["main"]["humidity"] for e in entries]
        wind = [e["wind"]["speed"] for e in entries]
        descriptions = [e["weather"][0]["description"] for e in entries]

        result.append(
            {
                "date": d,
                "temp_min": min(temps_min),
                "temp_max": max(temps_max),
                "humidity": int(sum(humidity) / len(humidity)),
                "wind_speed": sum(wind) / len(wind),
                "description": max(set(descriptions), key=descriptions.count),
            }
        )

    return result
