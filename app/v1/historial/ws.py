from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.v1.estados.repository import SensorRepository
import asyncio

ws_router = APIRouter()
repo = SensorRepository()

@ws_router.websocket("/ws/historial")
async def websocket_historial(websocket: WebSocket):
    await websocket.accept()
    try:
        last_timestamp = None
        while True:
          
            lecturas = repo.historial(999999999)  # Un número muy grande para no limitar
            if lecturas:
                current_last = lecturas[-1]["timestamp"]
                if current_last != last_timestamp:
                    await websocket.send_json({"total": len(lecturas), "lecturas": lecturas})
                    last_timestamp = current_last
        
    except WebSocketDisconnect:
        pass
