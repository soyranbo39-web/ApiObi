from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class SensorReading:
    temp: float
    hum: float
    co2: int
    dispositivo: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
