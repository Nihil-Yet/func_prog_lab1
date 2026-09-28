import os
from dotenv import load_dotenv

load_dotenv()


def _require(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise RuntimeError(f"{name} is not set")
    return value


DB_URL: str = _require("DB_URL")
DB_USER: str = _require("DB_USER")
DB_PASSWORD: str = _require("DB_PASSWORD")
WEATHER_API_KEY: str = _require("WEATHER_API_KEY")
WEATHER_API_URL: str = _require("WEATHER_API_BASE_URL")
GEO_API_URL: str | None = os.getenv("GEO_API_URL")

GEO_API_FALLBACK_CITY: str | None = os.getenv("GEO_API_FALLBACK_CITY")
ENVIRONMENT: str | None = os.getenv("ENVIRONMENT")
OUTPUT_FILE: str = os.getenv("OUTPUT_FILE", "output.md")
