from functools import lru_cache
from uuid import uuid4

from fastapi.websockets import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str : WebSocket] = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        id = str(uuid4())
        self.active_connections.update({id:websocket})
        return id

    async def send(self, id: str, msg: str):
        socket: WebSocket = self.active_connections[id]
        await socket.send_text(msg)

    def disconnect(self, key: str):
        self.active_connections.pop(key)

@lru_cache
def get_manager():
    return ConnectionManager()