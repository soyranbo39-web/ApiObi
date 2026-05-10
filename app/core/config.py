from pathlib import Path

MAX_HISTORIAL = 100
DEFAULT_HISTORIAL_LIMIT = 50

BASE_DIR = Path(__file__).resolve().parents[2]
SQLITE_DB_PATH = BASE_DIR / "data" / "apiobi.db"
DATABASE_URL = f"sqlite:///{SQLITE_DB_PATH}"
