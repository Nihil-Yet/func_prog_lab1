from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Float,
    Integer,
    String,
    UniqueConstraint,
    create_engine,
)
from sqlalchemy.engine import make_url
from sqlalchemy.orm import declarative_base, sessionmaker

from env_manager import DB_PASSWORD, DB_URL, DB_USER

url = make_url(DB_URL).set(username=DB_USER, password=DB_PASSWORD)
engine = create_engine(url)

Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Weather(Base):
    __tablename__ = "weather_forecast"
    __table_args__ = (
        UniqueConstraint("city", "forecast_date", name="uq_city_forecast_date"),
    )

    id = Column(Integer, primary_key=True)
    city = Column(String(100), nullable=False)
    forecast_date = Column(Date, nullable=False)
    temp_min = Column(Float)
    temp_max = Column(Float)
    humidity = Column(Integer)
    wind_speed = Column(Float)
    description = Column(String(100))
    created_at = Column(DateTime)

    def __repr__(self):
        return f"<Weather {self.city} {self.forecast_date}>"


def save_forecast(city: str, rows: list[dict]) -> list[Weather]:
    existing = {
        d
        for (d,) in session.query(Weather.forecast_date)
        .filter(Weather.city == city)
        .all()
    }

    saved: list[Weather] = []
    for row in rows:
        if row["date"] in existing:
            continue
        w = Weather(
            city=city,
            forecast_date=row["date"],
            temp_min=row["temp_min"],
            temp_max=row["temp_max"],
            humidity=row["humidity"],
            wind_speed=row["wind_speed"],
            description=row["description"],
            created_at=datetime.now(tz=timezone.utc),
        )
        session.add(w)
        saved.append(w)

    session.commit()
    return saved


Base.metadata.create_all(engine)
