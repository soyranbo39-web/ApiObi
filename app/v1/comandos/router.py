from fastapi import APIRouter

from app.v1.comandos.repository import CommandRepository

comandos_router = APIRouter()
repo            = CommandRepository()


@comandos_router.get("/comandos/pendientes")
def comandos_pendientes():
    pendientes = repo.pendientes()
    return {
        "total":    len(pendientes),
        "comandos": pendientes,
    }
