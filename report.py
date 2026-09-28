from env_manager import OUTPUT_FILE

HEADERS = [
    "Дата",
    "Мин. темп. (°C)",
    "Макс. темп. (°C)",
    "Описание",
    "Влажность (%)",
    "Ветер (м/с)",
]


def _row_from(r) -> list[str]:
    return [
        str(r.forecast_date),
        str(round(r.temp_min)),
        str(round(r.temp_max)),
        r.description.capitalize(),
        str(r.humidity),
        str(round(r.wind_speed)),
    ]


def _render(city: str, rows: list) -> str:
    if not rows:
        return f"# Прогноз погоды\n\nЛокация: {city}\n\nНет данных.\n"

    rows_sorted = sorted(rows, key=lambda r: r.forecast_date)
    body = [_row_from(r) for r in rows_sorted]

    widths = [len(h) for h in HEADERS]
    for row in body:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))

    def line(cells: list[str]) -> str:
        return "| " + " | ".join(c.ljust(widths[i]) for i, c in enumerate(cells)) + " |"

    separator = "|" + "|".join("-" * (w + 2) for w in widths) + "|"

    period = f"{rows_sorted[0].forecast_date} – {rows_sorted[-1].forecast_date}"

    out = [
        "# Прогноз погоды",
        f"Автоматически определённая локация: {city}",
        f"Период: {period}",
        "",
        line(HEADERS),
        separator,
    ]
    out.extend(line(row) for row in body)
    return "\n".join(out) + "\n"


def write_markdown(city: str, rows: list) -> None:
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(_render(city, rows))
