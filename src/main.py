from datetime import datetime, timedelta, timezone

from db_manager import Weather, save_forecast, session
from env_manager import OUTPUT_FILE
from geoloc import Location, get_location
from report import write_markdown
from weather_api import aggregate_daily, fetch_forecast


def print_summary(
    loc: Location,
    period_start,
    period_end,
    saved_count: int,
    output_path: str,
) -> None:
    sep = "=" * 50
    if loc.lat is not None and loc.lon is not None:
        coords = f"{loc.lat:.4f}, {loc.lon:.4f}"
    else:
        coords = "не определены"

    print(sep)
    print(f"  Город:            {loc.city}")
    print(f"  Координаты:       {coords}")
    print(f"  Период прогноза:  {period_start} – {period_end}")
    print(f"  Сохранено записей: {saved_count}")
    print(f"  Файл отчёта:      {output_path}")
    print(sep)


def main() -> int:
    loc = get_location()
    raw = fetch_forecast(loc)
    daily = aggregate_daily(raw, days=4)

    saved = save_forecast(loc.city, daily)

    today = datetime.now(tz=timezone.utc).date()
    period_end = today + timedelta(days=3)

    all_rows = (
        session.query(Weather)
        .filter(
            Weather.city == loc.city,
            Weather.forecast_date >= today,
            Weather.forecast_date <= period_end,
        )
        .order_by(Weather.forecast_date)
        .all()
    )

    write_markdown(loc.city, all_rows)

    period_start = all_rows[0].forecast_date if all_rows else "—"
    actual_period_end = all_rows[-1].forecast_date if all_rows else "—"

    print_summary(
        loc,
        period_start,
        actual_period_end,
        len(saved),
        OUTPUT_FILE,
    )

    return 0


if __name__ == "__main__":
    main()
