from typing import Dict, List
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}  # <--- было int

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)

    def disconnect(self, user_id: str, websocket: WebSocket):
        self.active_connections[user_id].remove(websocket)
        if not self.active_connections[user_id]:
            del self.active_connections[user_id]

    async def send_to_user(self, user_id: str, message: dict):
        for connection in self.active_connections.get(user_id, []):
            await connection.send_json(message)

manager = ConnectionManager()
