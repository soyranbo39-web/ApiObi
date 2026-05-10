from fastapi import APIRouter, Query

from app.core.config import DEFAULT_HISTORIAL_LIMIT, MAX_HISTORIAL
from app.v1.estados.repository import SensorRepository

historial_router = APIRouter()
repo             = SensorRepository()


@historial_router.get("/historial")
def obtener_historial(limit: int = Query(default=DEFAULT_HISTORIAL_LIMIT, ge=1, le=MAX_HISTORIAL)):
    lecturas = repo.historial(limit)
    return {"total": len(lecturas), "lecturas": lecturas}
