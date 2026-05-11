#!/usr/bin/env sh
set -e

# Render proporciona PORT; localmente se usa 8000 por defecto.
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
