from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.db import init_db
from app.v1.comandos.router import comandos_router
from app.v1.control.router import control_router
from app.v1.datos.router import datos_router
from app.v1.estados.router import estado_router
from app.v1.historial.router import historial_router


def create_app() -> FastAPI:
    app = FastAPI()
    init_db()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    for router in [datos_router, estado_router, historial_router, control_router, comandos_router]:
        app.include_router(router)

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=5000, reload=False)
