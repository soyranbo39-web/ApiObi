from fastapi import APIRouter

from app.v1.comandos.repository import CommandRepository
from app.v1.control.schemas import ControlIn
from app.v1.estados.repository import SensorRepository

control_router = APIRouter()
sensor_repo    = SensorRepository()
command_repo   = CommandRepository()


@control_router.post("/control")
def enviar_control(body: ControlIn):
    command_repo.encolar(body.actuador, body.accion)
    sensor_repo.set_modo("manual")
    return {
        "ok":       True,
        "actuador": body.actuador,
        "accion":   body.accion,
        "modo":     sensor_repo.modo,
    }
