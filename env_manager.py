import logging
import os

from dotenv import load_dotenv

load_dotenv()

LEVEL = os.getenv("LOG_LEVEL", "WARNING").upper()

logging.basicConfig(
    level=LEVEL,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

log = logging.getLogger(__name__)


def _require(name: str) -> str:
    v = os.getenv(name)
    if v is None:
        raise RuntimeError(f"{name} is not set")
    return v


DB_URL: str = _require("DB_URL")
DB_USER: str = os.getenv("DB_USER", "")
DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
WEATHER_API_KEY: str = _require("WEATHER_API_KEY")
WEATHER_API_URL: str = _require("WEATHER_API_BASE_URL")
GEO_API_URL: str | None = os.getenv("GEO_API_URL")

GEO_API_FALLBACK_CITY: str | None = os.getenv("GEO_API_FALLBACK_CITY")
ENVIRONMENT: str | None = os.getenv("ENVIRONMENT")
OUTPUT_FILE: str = os.getenv("OUTPUT_FILE", "weather_report.md")
