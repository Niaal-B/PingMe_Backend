from fastapi import WebSocket
from typing import Dict, List
import asyncio

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: str):
        """Add a new client to a room"""
        await websocket.accept()  
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)
        print(f"Client connected to {room_id}. Total: {len(self.active_connections[room_id])}")

    def disconnect(self, websocket: WebSocket, room_id: str):
        """Remove a client from a room"""
        if room_id in self.active_connections:
            self.active_connections[room_id].remove(websocket)
            if not self.active_connections[room_id]:  
                del self.active_connections[room_id]
            print(f"Client disconnected from {room_id}. Remaining: {len(self.active_connections.get(room_id, []))}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send a message to a specific client"""
        await websocket.send_text(message)

    async def broadcast(self, room_id: str, message: str):
        if room_id in self.active_connections:
            tasks = [connection.send_text(message) for connection in self.active_connections[room_id]]
            await asyncio.gather(*tasks)