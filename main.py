from db_manager import Weather, session
from env_manager import OUTPUT_FILE
from geoloc import get_location
from report import write_markdown
from weather_api import aggregate_daily, fetch_forecast


def main() -> int:
    loc = get_location()
    raw = fetch_forecast(loc)
    daily = aggregate_daily(raw, days=4)

    session.query(Weather).filter(Weather.city == loc.city).delete()

    saved = []
    for row in daily:
        w = Weather(
            city=loc.city,
            forecast_date=row["date"],
            temp_min=row["temp_min"],
            temp_max=row["temp_max"],
            humidity=row["humidity"],
            wind_speed=row["wind_speed"],
            description=row["description"],
        )
        session.add(w)
        saved.append(w)

    session.commit()
    write_markdown(loc.city, saved)
    print(f"Готово: {len(saved)} записей → {OUTPUT_FILE}")
    return 0


if __name__ == "__main__":
    main()
