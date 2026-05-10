# ApiObi
fastapi dev app/main.py --host 0.0.0.0 --port 8000    

## Seguridad

La API requiere API Key en todos los endpoints.

- Header por defecto: `X-API-Key`
- Valor por defecto: `cambiar-esta-api-key`

Puedes cambiar ambos con variables de entorno:

- `API_KEY_HEADER_NAME`
- `API_KEY_VALUE`

## Configuracion para ESP32

Levanta la API escuchando en la red local (no solo localhost):

```bash
fastapi dev app/main.py --host 0.0.0.0 --port 8000
```

Base URL en firmware (ejemplo):

- `http://192.168.50.211:8000`

Pruebas rapidas desde la misma red:

```bash
curl http://192.168.50.211:8000/health
curl -X POST http://192.168.50.211:8000/auth/token -H "Content-Type: application/x-www-form-urlencoded" -d "username=admin&password=123456"
```

Si no conecta:

- Verifica que el servidor este corriendo con `--host 0.0.0.0`.
- Verifica que el puerto `8000` no este bloqueado por firewall.
- Asegura que ESP32 y PC esten en la misma red/subred.