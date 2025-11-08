import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status,Depends
from app.websocket.connection_manager import ConnectionManager
from app.utils.jwt import decode_access_token 
from app.models.user import User
from app.database import get_db
from sqlalchemy.orm import Session
from datetime import datetime


router = APIRouter()
manager = ConnectionManager()

async def ws_get_current_user(token: str, db: Session):
    payload = decode_access_token(token)
    user_id = payload["sub"]

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise Exception("User not found")

    return user



@router.websocket("/ws/rooms/{room_id}")
async def websocket_room_endpoint(websocket: WebSocket, room_id: int, db: Session = Depends(get_db)):
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    try:
        user = await ws_get_current_user(token, db)
        print("User decoded:", user.id, user.username)
    except Exception as e:
        print("Token decode failed:", e)
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await manager.connect(room_id, websocket, user.id)
    await manager.broadcast_excluding(room_id, {
        "type": "join",
        "payload": {
            "sender_id": user.id,
            "sender_name": user.username
        }
    }, websocket)
    await manager.send_personal(websocket, {
        "type": "history",
        "payload": await manager.get_history(room_id)
    })

    try:
        while True:
            raw = await websocket.receive_text()
            data = json.loads(raw)
            print("Received:", data)

            message_type = data.get("type")

            # Handle typing indicators
            if message_type == "typing_start":
                await manager.broadcast_excluding(room_id, {
                    "type": "typing_start",
                    "payload": {
                        "sender_id": user.id,
                        "sender_name": user.username
                    }
                }, websocket)
                continue
            elif message_type == "typing_stop":
                await manager.broadcast_excluding(room_id, {
                    "type": "typing_stop",
                    "payload": {
                        "sender_id": user.id,
                        "sender_name": user.username
                    }
                }, websocket)
                continue

            # Handle regular messages
            if message_type != "message" or not data.get("payload", {}).get("content"):
                await manager.send_personal(websocket, {
                    "type": "error",
                    "payload": { "detail": "Invalid message format." }
                })
                continue

            # Send typing_stop when message is sent
            await manager.broadcast_excluding(room_id, {
                "type": "typing_stop",
                "payload": {
                    "sender_id": user.id,
                    "sender_name": user.username
                }
            }, websocket)

            message = {
                "room_id": room_id,
                "sender_id": user.id,
                "sender_name": user.username,
                "content": data["payload"]["content"],
                "timestamp": datetime.now().isoformat()
            }

            await manager.append_message(room_id, message)
            await manager.broadcast(room_id, {
                "type": "message",
                "payload": message
            })
            print("Broadcasted:", message)

    except WebSocketDisconnect:
        await manager.disconnect(room_id, websocket)
        await manager.broadcast_excluding(room_id, {
            "type": "leave",
            "payload": {
                "sender_id": user.id,
                "sender_name": user.username
            }
        }, websocket)
