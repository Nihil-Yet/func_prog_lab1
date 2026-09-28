# Weather Forecast

## Описание

Скрипт определяет текущую локацию пользователя по IP, запрашивает прогноз погоды
на 4 дня (сегодня + 3) и сохраняет результат в SQLite и в Markdown-файл.

- **OpenWeatherMap** (`/data/2.5/forecast`) — прогноз на 5 дней с шагом 3 часа.
  Бесплатный тариф, ключ без привязки карты.
- IP-геолокация (город + координаты)
  Если IP не сработал — работает по имени города из `GEO_API_FALLBACK_CITY`.

Библиотеки:

| Пакет         | Версия |
|---------------|--------|
| requests      | 2.34.2 |
| SQLAlchemy    | 2.0.54 |
| python-dotenv | 1.2.3  |

---

## Установка

```bash
git clone https://github.com/Nihil-Yet/func_prog_lab1.git 
cd func_prog_lab1
cp .env.example .env
```

### Быстрый старт

```bash
chmod +x run.sh
./run.sh
```

### Ручной запуск

```bash
python -m venv .venv
source .venv/bin/activate          # Linux / macOS
# .venv\Scripts\activate           # Windows

pip install -r requirements.txt
python src/main.py
```


---

## Настройка

1. Скопируйте шаблон: `cp .env.example .env`

2. Зарегистрируйтесь на [openweathermap.org](https://openweathermap.org/),
   получите бесплатный API-ключ в разделе *API keys* и вставьте его в `WEATHER_API_KEY`.

3. Заполните `.env`:

   ```env
   DB_URL=sqlite:///./weather.db
   DB_USER=
   DB_PASSWORD=

   WEATHER_API_KEY=ключ
   WEATHER_API_BASE_URL=https://api.openweathermap.org/data/2.5

   GEO_API_URL=https://ip-api.com/json/
   GEO_API_FALLBACK_CITY=ЗапаснойГород

   ENVIRONMENT=""
   LOG_LEVEL=WARNING
   OUTPUT_FILE=output.md
   ```

   - `WEATHER_API_KEY` — обязателен.
   - `GEO_API_FALLBACK_CITY` — город, который используется, если IP-геолокация не сработала.
   - `LOG_LEVEL` — `DEBUG` / `INFO` / `WARNING` / `ERROR` / `CRITICAL`.
   - `OUTPUT_FILE` — путь к Markdown-файлу с отчётом.


---

## Структура проекта

- `main.py` — точка входа: определяет локацию, тянет прогноз, сохраняет в БД, пишет отчёт, печатает сводку.
- `env_manager.py` — загрузка и валидация переменных окружения из `.env`, общий логгер.
- `geoloc.py` — определение локации: IP-геолокация → фолбэк по имени города.
- `weather_api.py` — запрос прогноза к OpenWeatherMap и агрегация 3-часовых точек в дневные записи.
- `db_manager.py` — подключение к БД, модель `Weather`, сохранение без дубликатов по паре (город, дата).
- `report.py` — рендер Markdown-отчёта с выравниванием колонок.
- `requirements.txt` — зависимости проекта.
- `.env.example` — шаблон конфигурации.
- `run.sh` — установка и запуск одной командой.

---

## Пример вывода

### Markdown-отчёт

# Прогноз погоды
Автоматически определённая локация: Kirov
Период: 2026-09-28 – 2026-10-01

| Дата       | Мин. темп. (°C) | Макс. темп. (°C) | Описание | Влажность (%) | Ветер (м/с) |
|------------|-----------------|------------------|----------|---------------|-------------|
| 2026-09-28 | 8               | 9                | Ясно     | 91            | 2           |
| 2026-09-29 | 5               | 16               | Ясно     | 77            | 3           |
| 2026-09-30 | 4               | 16               | Ясно     | 78            | 2           |
| 2026-10-01 | 6               | 15               | Пасмурно | 77            | 3           |

### Консольная сводка
```bash
==================================================
  Город:            Frankfurt am Main
  Координаты:       50.0827, 8.6297
  Период прогноза:  2026-09-28 – 2026-10-01
  Сохранено записей: 0
  Файл отчёта:      weather_report.md
==================================================
```
