from sqlalchemy import select

from app.core.db import SessionLocal
from app.model.command_orm import CommandORM


class CommandRepository:
	def encolar(self, actuador: str, accion: str) -> CommandORM:
		with SessionLocal() as db:
			command = CommandORM(actuador=actuador, accion=accion)
			db.add(command)
			db.commit()
			db.refresh(command)
			return command

	def pendientes(self) -> list[dict]:
		with SessionLocal() as db:
			pending_commands = list(
				db.execute(
					select(CommandORM).where(CommandORM.entregado.is_(False))
				).scalars()
			)
			for command in pending_commands:
				command.entregado = True
			db.commit()
			return [CommandORM._serialize_command(command) for command in pending_commands]

	def todos(self) -> list[dict]:
		with SessionLocal() as db:
			commands = list(db.execute(select(CommandORM)).scalars())
			return [CommandORM._serialize_command(command) for command in commands]
