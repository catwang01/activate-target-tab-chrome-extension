import asyncio
import websockets

async def receive_websocket_message():
    async with websockets.connect('ws://localhost:8080') as websocket:  # Replace with your WebSocket server URL
        while True:
            message = await websocket.recv()
            print(f"Received message: {message}")
            await websocket.send(f"hello {message}")
            # Process the message as needed, e.g., activate the tab

asyncio.get_event_loop().run_until_complete(receive_websocket_message())
