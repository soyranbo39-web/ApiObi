from typing import Annotated

from fastapi import APIRouter, Query

from app.core.config import DEFAULT_HISTORIAL_LIMIT, MAX_HISTORIAL
from app.v1.estados.repository import SensorRepository

historial_router = APIRouter(tags=["historial"])
repo             = SensorRepository()


@historial_router.get("/historial")
def obtener_historial(
    limit: Annotated[int, Query(ge=1, le=MAX_HISTORIAL)] = DEFAULT_HISTORIAL_LIMIT,
):
    lecturas = repo.historial(limit)
    return {"total": len(lecturas), "lecturas": lecturas}
