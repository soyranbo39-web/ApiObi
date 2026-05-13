import fastapi
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse

from app.core.db import init_db
from app.core.security import require_authenticated_user
from app.v1.auth.router import auth_router
from app.v1.comandos.router import comandos_router
from app.v1.control.router import control_router
from app.v1.datos.router import datos_router
from app.v1.estados.router import estado_router
from app.v1.historial.router import historial_router

_SWAGGER_JS = """
<script>
(function persistSwaggerAuth() {
  const STORAGE_KEY = "swagger_oauth2_token";

  function waitForSwagger(cb, tries = 0) {
    if (typeof window.ui !== "undefined") { cb(); }
    else if (tries < 40) { setTimeout(() => waitForSwagger(cb, tries + 1), 250); }
  }

  waitForSwagger(() => {
    // Restaurar token guardado
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      window.ui.preauthorizeApiKey
        ? window.ui.preauthorizeApiKey("OAuth2PasswordBearer", saved)
        : window.ui.authActions.authorize({
            OAuth2PasswordBearer: { name: "OAuth2PasswordBearer", schema: { type: "apiKey", in: "header" }, value: saved }
          });
      window.ui.preauthorizeApiKey && window.ui.preauthorizeApiKey("OAuth2PasswordBearer", saved);
      // Para OAuth2 bearer
      window.ui.authActions && window.ui.authActions.authorize({
        OAuth2PasswordBearer: {
          name: "OAuth2PasswordBearer",
          schema: { type: "oauth2", flows: {} },
          value: saved,
        },
      });
    }

    // Interceptar guardado del token al hacer Authorize
    const origAuthorize = window.ui.authActions && window.ui.authActions.authorize;
    if (origAuthorize) {
      window.ui.authActions.authorize = function(args) {
        const val = args && args.OAuth2PasswordBearer && args.OAuth2PasswordBearer.value;
        if (val) { localStorage.setItem(STORAGE_KEY, val); }
        return origAuthorize.call(this, args);
      };
    }

    // Interceptar logout para limpiar localStorage
    const origLogout = window.ui.authActions && window.ui.authActions.logout;
    if (origLogout) {
      window.ui.authActions.logout = function(args) {
        if (args && args.includes && args.includes("OAuth2PasswordBearer")) {
          localStorage.removeItem(STORAGE_KEY);
        }
        return origLogout.call(this, args);
      };
    }
  });
})();
</script>
"""


def create_app() -> FastAPI:
    app = FastAPI(docs_url=None) 
    init_db()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    @app.get("/docs", include_in_schema=False)
    def custom_swagger_ui() -> HTMLResponse:
        html = get_swagger_ui_html(openapi_url="/openapi.json", title="ApiObi")
        body = html.body.decode()
        body = body.replace("</body>", f"{_SWAGGER_JS}</body>")
        return HTMLResponse(body)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    app.include_router(auth_router)


    from app.v1.historial.ws import ws_router
    app.include_router(ws_router)

    for router in [datos_router, estado_router, historial_router, control_router, comandos_router]:
      app.include_router(router, dependencies=[Depends(require_authenticated_user)])

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
