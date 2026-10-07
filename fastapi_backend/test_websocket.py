import asyncio
import websockets


async def test_websocket():
    uri = "ws://127.0.0.1:8001/ws/notifications/1"

    async with websockets.connect(uri) as websocket:
        print("WebSocket connected")
        print("Waiting for notification...")

        while True:
            message = await websocket.recv()
            print("Received:", message)


asyncio.run(test_websocket())