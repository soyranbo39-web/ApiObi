import uuid
from dataclasses import dataclass, field


@dataclass
class Command:
    actuador: str
    accion: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    entregado: bool = False
