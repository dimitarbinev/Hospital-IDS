from fastapi import APIRouter, WebSocket,  WebSocketDisconnect

webSocket_router = APIRouter()

@webSocket_router.websocket("/ws")
