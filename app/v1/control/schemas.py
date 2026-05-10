from pydantic import BaseModel, field_validator

from app.model.actuator import VALID_ACTUATORS, VALID_STATES


class ControlIn(BaseModel):
    actuador: str
    accion: str

    @field_validator("actuador")
    @classmethod
    def validar_actuador(cls, v: str) -> str:
        v = v.lower()
        if v not in VALID_ACTUATORS:
            raise ValueError(f"Actuador inválido. Válidos: {VALID_ACTUATORS}")
        return v

    @field_validator("accion")
    @classmethod
    def validar_accion(cls, v: str) -> str:
        v = v.upper()
        if v not in VALID_STATES:
            raise ValueError(f"Acción inválida. Válidas: {VALID_STATES}")
        return v
