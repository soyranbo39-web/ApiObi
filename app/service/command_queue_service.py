from typing import Optional

from app.model.command import Command


class CommandQueueService:
    _instance: Optional["CommandQueueService"] = None

    def __new__(cls) -> "CommandQueueService":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._queue: list[Command] = []
        return cls._instance

    def encolar(self, actuador: str, accion: str) -> Command:
        command = Command(actuador=actuador, accion=accion)
        self._queue.append(command)
        return command

    def pendientes(self) -> list[Command]:
        no_entregados = [c for c in self._queue if not c.entregado]
        for command in no_entregados:
            command.entregado = True
        return no_entregados

    def todos(self) -> list[Command]:
        return list(self._queue)
