from fastapi import APIRouter

from app.v1.estados.repository import SensorRepository

estado_router = APIRouter()
repo          = SensorRepository()


@estado_router.get("/estado")
def obtener_estado():
    ultima = repo.ultima_lectura()

    sensores = {}
    if ultima:
        sensores = {"temp": ultima.temp, "hum": ultima.hum, "co2": ultima.co2}

    return {
        "sensores":      sensores,
        "actuadores":    repo.estado_actuadores(),
        "modo":          repo.modo,
        "ultimo_update": repo.ultimo_update(),
    }
