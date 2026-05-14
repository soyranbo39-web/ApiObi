from fastapi import APIRouter

from app.v1.estados.repository import SensorRepository

historial_router = APIRouter(tags=["historial"])
repo = SensorRepository()

@historial_router.get("/historial")
def obtener_historial():
    lecturas = repo.historial()
    return {"total": len(lecturas), "lecturas": lecturas}
