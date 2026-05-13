import os
from pathlib import Path

MAX_HISTORIAL = 1000
DEFAULT_HISTORIAL_LIMIT = 50

BASE_DIR = Path(__file__).resolve().parents[2]
SQLITE_DB_PATH = BASE_DIR / "data" / "apiobi.db"
DATABASE_URL = f"sqlite:///{SQLITE_DB_PATH}"

API_KEY_HEADER_NAME = os.getenv("API_KEY_HEADER_NAME", "X-API-Key")
API_KEY_VALUE = os.getenv("API_KEY_VALUE", "cambiar-esta-api-key")

AUTH_SECRET_KEY = os.getenv("AUTH_SECRET_KEY", "cambiar-esta-clave-secreta-auth")
AUTH_TOKEN_EXPIRE_MINUTES = int(os.getenv("AUTH_TOKEN_EXPIRE_MINUTES", "30"))
AUTH_JWT_ALGORITHM = os.getenv("AUTH_JWT_ALGORITHM", "HS256")
AUTH_COOKIE_NAME = os.getenv("AUTH_COOKIE_NAME", "access_token")
AUTH_COOKIE_SECURE = os.getenv("AUTH_COOKIE_SECURE", "false").lower() == "true"
