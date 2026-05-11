from pydantic import BaseModel


class DatosIn(BaseModel):
    temp: float
    hum: float
    co2: int
    dispositivo: str
    riego: str | None = None
    ventilador: str | None = None
