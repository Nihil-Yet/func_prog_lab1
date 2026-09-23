from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Date
from sqlalchemy.orm import declarative_base, sessionmaker

from dotenv import load_dotenv
import os

load_dotenv()
db_url = os.getenv("DATABASE_URL")

engine = create_engine(db_url, echo=True)

Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


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
        return f"<Weather {self.city} {self.temp}>"


Base.metadata.create_all(engine)


def main():
    print("Hello!")
    return 0


if __name__ == "__main__":
    main()
