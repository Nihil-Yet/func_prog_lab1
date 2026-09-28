from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Date
from sqlalchemy.orm import declarative_base, sessionmaker

from env_manager import DB_URL


engine = create_engine(DB_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Weather(Base):
    __tablename__ = "weather_forecast"

    id = Column(Integer, primary_key=True)
    city = Column(String(100), nullable=False)
    forecast_date = Column(Date)
    temp_min = Column(Float)
    temp_max = Column(Float)
    humidity = Column(Integer)
    wind_speed = Column(Float)
    description = Column(String(100))
    created_at = Column(DateTime)

    def __repr__(self):
        return f"<Weather {self.city} {self.temp_max}>"


Base.metadata.create_all(engine)
