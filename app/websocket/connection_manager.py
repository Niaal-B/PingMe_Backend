from collections import defaultdict, deque
from typing import Dict, Set, Deque
from fastapi import WebSocket
import json

class ConnectionManager:
    def __init__(self):
        self.connections: Dict[int, Set[WebSocket]] = defaultdict(set)
        self.messages: Dict[int, Deque[dict]] = defaultdict(lambda: deque(maxlen=100))

    async def connect(self, room_id: int, websocket: WebSocket):
        await websocket.accept()
        self.connections[room_id].add(websocket)

    async def disconnect(self, room_id: int, websocket: WebSocket):
        self.connections[room_id].discard(websocket)
        if not self.connections[room_id]:
            self.connections.pop(room_id, None)
            self.messages.pop(room_id, None)

    async def append_message(self, room_id: int, message: dict):
        self.messages[room_id].append(message)

    async def get_history(self, room_id: int) -> list:
        return list(self.messages.get(room_id, []))

    async def broadcast(self, room_id: int, payload: dict):
        text = json.dumps(payload)
        connections = list(self.connections.get(room_id, []))
        for conn in connections:
            try:
                await conn.send_text(text)
            except Exception:
                pass 

    async def send_personal(self, websocket: WebSocket, payload: dict):
        await websocket.send_text(json.dumps(payload))
