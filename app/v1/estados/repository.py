from dataclasses import asdict, is_dataclass

from sqlalchemy import select

from app.core.db import SessionLocal
from app.model.actuator import VALID_ACTUATORS, VALID_STATES
from app.model.actuator_state_orm import ActuatorStateORM
from app.model.app_state_orm import AppStateORM
from app.model.sensor_reading_orm import SensorReadingORM


class SensorRepository:
	def _ensure_defaults(self, db) -> None:
		if db.get(AppStateORM, "modo") is None:
			db.add(AppStateORM(key="modo", value="automatico"))

		for actuator_name in VALID_ACTUATORS:
			if db.get(ActuatorStateORM, actuator_name) is None:
				db.add(ActuatorStateORM(name=actuator_name, state="OFF"))

		db.commit()

	def guardar_lectura(self, reading) -> SensorReadingORM:
		payload = reading.model_dump() if hasattr(reading, "model_dump") else asdict(reading) if is_dataclass(reading) else dict(reading)
		with SessionLocal() as db:
			self._ensure_defaults(db)
			sensor_reading = SensorReadingORM(**payload)
			db.add(sensor_reading)
			db.commit()
			db.refresh(sensor_reading)
			return sensor_reading

	def ultima_lectura(self):
		with SessionLocal() as db:
			return db.execute(
				select(SensorReadingORM).order_by(SensorReadingORM.id.desc())
			).scalars().first()

	def historial(self, limit: int):
		with SessionLocal() as db:
			readings = list(
				db.execute(
					select(SensorReadingORM)
					.order_by(SensorReadingORM.id.desc())
					.limit(limit)
				).scalars()
			)
			readings.reverse()
			return [SensorReadingORM._serialize_reading(reading) for reading in readings]

	def set_actuador(self, nombre: str, estado: str) -> None:
		estado = estado.upper()
		if nombre not in VALID_ACTUATORS or estado not in VALID_STATES:
			return

		with SessionLocal() as db:
			self._ensure_defaults(db)
			actuator = db.get(ActuatorStateORM, nombre)
			if actuator:
				actuator.state = estado
				db.commit()

	def estado_actuadores(self):
		with SessionLocal() as db:
			self._ensure_defaults(db)
			actuators = list(db.execute(select(ActuatorStateORM)).scalars())
			return {actuator.name: actuator.state for actuator in actuators}

	@property
	def modo(self):
		with SessionLocal() as db:
			self._ensure_defaults(db)
			mode = db.get(AppStateORM, "modo")
			return mode.value if mode else "automatico"

	def set_modo(self, modo: str):
		if modo not in ("automatico", "manual"):
			return

		with SessionLocal() as db:
			self._ensure_defaults(db)
			mode = db.get(AppStateORM, "modo")
			if mode:
				mode.value = modo
				db.commit()

	def ultimo_update(self):
		latest = self.ultima_lectura()
		if latest and latest.timestamp:
			return latest.timestamp.isoformat()
		return None
