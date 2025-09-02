import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, Set, Literal

from fastapi import WebSocket, WebSocketDisconnect, APIRouter

from Backend.rest.service.token_service import get_refresh_token
from Backend.rest.model.database import DB
from Backend.rest.schema.token_schema import RefreshTokenDTO

class WSManager:
    def __init__(self) -> None:
        self._clients: Set[WebSocket] = set()
        self._lock = asyncio.Lock()

    async def connect(self, ws: WebSocket) -> None:
        await ws.accept()
        async with self._lock:
            self._clients.add(ws)

    async def disconnect(self, ws: WebSocket) -> None:
        async with self._lock:
            self._clients.discard(ws)

    # copy of the current clients
    # safer way to get the current clients

    async def snapshot(self) -> list[WebSocket]:
        async with self._lock:
            return list(self._clients)

    async def broadcast(self, payload: Dict[str, Any]) -> None:
        clients = await self.snapshot()
        if not clients:
            return
        to_drop: list[WebSocket] = []
        for ws in clients:
            try:
                await ws.send_json(payload)
            except Exception:
                to_drop.append(ws)
        for ws in to_drop:
            await self.disconnect(ws)

manager = WSManager()

def verify_token(token: str, refreshTokenDTO: RefreshTokenDTO) -> bool:
    saved_refresh_token = get_refresh_token(refreshTokenDTO, DB)
    if saved_refresh_token.refresh_token == token:
        return True
    return False

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

'''
alert for the status of the device 
event for finding out what is the exact problem
heartbeat for keep alive the device
'''

async def push(type_: Literal["alert","event","heartbeat"], data: Dict[str, Any]) -> None:

    await manager.broadcast({
        "type": type_,
        "at": _now_iso(),
        "data": data,
    })