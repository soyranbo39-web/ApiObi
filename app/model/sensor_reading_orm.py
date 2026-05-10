from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class SensorReadingORM(Base):
    __tablename__ = "sensor_readings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    temp: Mapped[float] = mapped_column(Float, nullable=False)
    hum: Mapped[float] = mapped_column(Float, nullable=False)
    co2: Mapped[int] = mapped_column(Integer, nullable=False)
    dispositivo: Mapped[str] = mapped_column(String(100), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    @staticmethod
    def _serialize_reading(reading: "SensorReadingORM") -> dict:
        return {
            "temp": reading.temp,
            "hum": reading.hum,
            "co2": reading.co2,
            "dispositivo": reading.dispositivo,
            "timestamp": reading.timestamp.isoformat() if reading.timestamp else None,
        }
