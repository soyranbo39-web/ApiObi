from fastapi import APIRouter

from app.model.sensor_reading import SensorReading
from app.v1.datos.schemas import DatosIn
from app.v1.estados.repository import SensorRepository

datos_router = APIRouter()
repo         = SensorRepository()


@datos_router.post("/datos", status_code=201)
def recibir_datos(body: DatosIn):
    reading = SensorReading(**body.model_dump())
    repo.guardar_lectura(reading)
    return {"ok": True, "timestamp": reading.timestamp}
