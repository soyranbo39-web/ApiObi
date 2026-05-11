from fastapi import APIRouter

from app.v1.estados.repository import SensorRepository

estado_router = APIRouter()
repo          = SensorRepository()


@estado_router.get("/estado")
def obtener_estado():
    return repo.estado_completo()
