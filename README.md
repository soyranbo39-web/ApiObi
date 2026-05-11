# ApiObi

## Documentacion en Render

Cuando el servicio este desplegado en Render, la documentacion de la API se puede abrir en:

- `https://<tu-servicio>.onrender.com/docs`
- `https://<tu-servicio>.onrender.com/openapi.json`

Tambien hay un endpoint de salud para validar que el deploy esta activo:

- `https://<tu-servicio>.onrender.com/health`

## Ver el historial de lecturas

El historial esta disponible en el endpoint protegido:

- `GET /historial`

Parametro disponible:

- `limit` (opcional): cantidad de lecturas a devolver.
	- Minimo: `1`
	- Maximo: `100`
	- Default: `50`

### Flujo recomendado en Render (Swagger)

1. Abre `https://<tu-servicio>.onrender.com/docs`.
2. Registra usuario en `POST /auth/register` (si aun no existe).
3. Inicia sesion en `POST /auth/token` para obtener `access_token`.
4. Haz clic en `Authorize` y pega el token.
5. Ejecuta `GET /historial`.

### Ejemplo con cURL

```bash
# 1) Obtener token
curl -X POST "https://<tu-servicio>.onrender.com/auth/token" \
	-H "Content-Type: application/x-www-form-urlencoded" \
	-d "username=tu_usuario&password=tu_password"

# 2) Consultar historial
curl "https://<tu-servicio>.onrender.com/historial?limit=20" \
	-H "Authorization: Bearer <access_token>"
```
