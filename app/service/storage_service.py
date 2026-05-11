from collections import deque
from datetime import datetime, timezone
from typing import Optional

from app.core.config import MAX_HISTORIAL
from app.model.actuator import Actuator
from app.model.sensor_reading import SensorReading


class StorageService:
    _instance: Optional["StorageService"] = None

    def __new__(cls) -> "StorageService":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self) -> None:
        self._historial: deque[SensorReading] = deque(maxlen=MAX_HISTORIAL)
        self._ultima_lectura: Optional[SensorReading] = None
        self._modo: str = "automatico"
        self._actuadores: dict[str, Actuator] = {
            "riego": Actuator("riego"),
            "ventilador": Actuator("ventilador"),
        }

    def guardar_lectura(self, reading: SensorReading) -> None:
        self._ultima_lectura = reading
        self._historial.append(reading)

    def ultima_lectura(self) -> Optional[SensorReading]:
        return self._ultima_lectura

    def historial(self, limit: int) -> list[dict]:
        items = list(self._historial)
        return [r.to_dict() for r in items[-limit:]]

    def set_actuador(self, nombre: str, estado: str) -> None:
        if nombre in self._actuadores:
            estado_normalizado = estado.upper()
            if estado_normalizado in {"ON", "OFF"}:
                self._actuadores[nombre].state = estado_normalizado

    def estado_actuadores(self) -> dict:
        return {nombre: act.state for nombre, act in self._actuadores.items()}

    @property
    def modo(self) -> str:
        return self._modo

    def set_modo(self, modo: str) -> None:
        if modo in ("automatico", "manual"):
            self._modo = modo

    def ultimo_update(self) -> Optional[str]:
        if self._ultima_lectura:
            return self._ultima_lectura.timestamp
        return None
