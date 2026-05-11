from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class ActuatorStateORM(Base):
    __tablename__ = "actuator_states"

    name: Mapped[str] = mapped_column(String(50), primary_key=True)
    state: Mapped[str] = mapped_column(String(10), nullable=False, default="OFF")
