from fastapi import APIRouter, WebSocket

router = APIRouter()

@router.websocket("/ws/test")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("🔌 Client connected")

    while True:
        data = await websocket.receive_text()
        print(f"📩 Received message: {data}")

        await websocket.send_text(f"Echo: {data}")
