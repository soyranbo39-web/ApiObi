import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class CommandORM(Base):
    __tablename__ = "commands"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    actuador: Mapped[str] = mapped_column(String(50), nullable=False)
    accion: Mapped[str] = mapped_column(String(10), nullable=False)
    entregado: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    @staticmethod
    def _serialize_command(command: "CommandORM") -> dict:
        return {
            "id": command.id,
            "actuador": command.actuador,
            "accion": command.accion,
            "entregado": command.entregado,
        }
