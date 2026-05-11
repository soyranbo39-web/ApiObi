from fastapi import APIRouter

from app.model.sensor_reading import SensorReading
from app.v1.datos.schemas import DatosIn
from app.v1.estados.repository import SensorRepository

datos_router = APIRouter()
repo         = SensorRepository()


@datos_router.post("/datos", status_code=201)
def recibir_datos(body: DatosIn):
    reading = SensorReading(
        temp=body.temp,
        hum=body.hum,
        co2=body.co2,
        dispositivo=body.dispositivo,
    )
    repo.guardar_lectura(reading)

    if body.riego is not None:
        repo.set_actuador("riego", body.riego)
    if body.ventilador is not None:
        repo.set_actuador("ventilador", body.ventilador)

    return {"ok": True, "timestamp": reading.timestamp}
