from collections import defaultdict, deque
from typing import Dict, Set, Deque
from fastapi import WebSocket
import json

class ConnectionManager:
    def __init__(self):
        self.connections: Dict[int, Set[WebSocket]] = defaultdict(set)
        self.messages: Dict[int, Deque[dict]] = defaultdict(lambda: deque(maxlen=100))
        self.websocket_to_user: Dict[WebSocket, int] = {}  # Track which websocket belongs to which user

    async def connect(self, room_id: int, websocket: WebSocket, user_id: int = None):
        await websocket.accept()
        self.connections[room_id].add(websocket)
        if user_id is not None:
            self.websocket_to_user[websocket] = user_id

    async def disconnect(self, room_id: int, websocket: WebSocket):
        self.connections[room_id].discard(websocket)
        self.websocket_to_user.pop(websocket, None)  # Clean up user mapping
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

    async def broadcast_excluding(self, room_id: int, payload: dict, exclude_websocket: WebSocket):
        """Broadcast to all connections in a room except the specified websocket"""
        text = json.dumps(payload)
        connections = list(self.connections.get(room_id, []))
        for conn in connections:
            if conn != exclude_websocket:
                try:
                    await conn.send_text(text)
                except Exception:
                    pass 

    async def send_personal(self, websocket: WebSocket, payload: dict):
        await websocket.send_text(json.dumps(payload))
