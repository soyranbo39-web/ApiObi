from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import SQLITE_DB_PATH


class Base(DeclarativeBase):
    pass


SQLITE_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
DATABASE_URL = f"sqlite:///{SQLITE_DB_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    from app.model.actuator import VALID_ACTUATORS
    from app.model.actuator_state_orm import ActuatorStateORM
    from app.model.app_state_orm import AppStateORM
    from app.model.command_orm import CommandORM  # noqa: F401
    from app.model.sensor_reading_orm import SensorReadingORM  # noqa: F401
    from app.model.user_orm import UserORM  # noqa: F401

    Base.metadata.create_all(bind=engine)

    with engine.begin() as conn:
        conn.exec_driver_sql("PRAGMA journal_mode=WAL;")
        conn.exec_driver_sql("PRAGMA synchronous=NORMAL;")
        conn.exec_driver_sql("PRAGMA cache_size=-32000;")
        conn.exec_driver_sql("PRAGMA temp_store=MEMORY;")
        conn.exec_driver_sql("PRAGMA busy_timeout=5000;")

    with SessionLocal() as db:
        if db.get(AppStateORM, "modo") is None:
            db.add(AppStateORM(key="modo", value="automatico"))

        for actuator_name in VALID_ACTUATORS:
            if db.get(ActuatorStateORM, actuator_name) is None:
                db.add(ActuatorStateORM(name=actuator_name, state="OFF"))

        db.commit()
