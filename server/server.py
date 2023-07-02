import asyncio
import json
from pathlib import Path
from typing import Optional, TypedDict

import keyboard
import websockets
from log import setupLogger
from environment import global_environ
from window_manager import IWindowManager, MacOsWindowManager, WindowsWindowManager
from utils import detect_system

Path('logs').mkdir(exist_ok=True, parents=True)
logger = setupLogger(__file__)
targetUrl = global_environ.targetUrl

current_system = detect_system()
if current_system == "Windows":
    combination = "ctrl+shift+J"
    detect_window_title = "Microsoft​ Edge"
elif current_system == "MacOs":
    combination = "command+J"
    detect_window_title = "Google Chrome"

window_manager: Optional[IWindowManager] = None
if  current_system == "Windows":
    window_manager = WindowsWindowManager()
elif current_system == "MacOs":
    window_manager = MacOsWindowManager()

def on_hotkey_press():
    try:
        logger.info(f"Key combination '{combination}' was pressed.")
        shouldContinue = window_manager.activate_window(detect_window_title)
        if shouldContinue:
            asyncio.run(activate_tab())
    except Exception as e:
        logger.error("Run into error", exc_info=e)

keyboard.add_hotkey(combination, on_hotkey_press)

class Message(TypedDict):
    action: str
    tabUrl: str

connected_clients = set()
queue: list[Message] = []

async def handle_websocket(websocket, path):
    connected_clients.add(websocket)
    await send(websocket, {"message": "The connection is created"})
    while True:
        logger.debug("Current queue size %s", len(queue))
        if queue:
            message = queue.pop(0)
            await send(websocket, message)
        try:
            await asyncio.wait_for(websocket.recv(), 1)
        except asyncio.exceptions.TimeoutError:
            pass
        except websockets.exceptions.ConnectionClosedError:
            logger.info("Exit due to connection closed")
            break
        except Exception as e:
            logger.error("Accept an unexpected error", exc_info=e)
            break

async def send(websocket, message):
    payload = json.dumps(message)
    logger.info(f"Sending message to clients: {payload}")
    await websocket.send(payload)

async def activate_tab():
    message: Message = {"action": "activateTab", "tabUrl": targetUrl}
    logger.info("Add a new message to the queue")
    queue.append(message)

start_server = websockets.serve(handle_websocket, "localhost", 8080) # type: ignore
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()