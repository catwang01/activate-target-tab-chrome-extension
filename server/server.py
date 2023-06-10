import asyncio
import json
import platform

import keyboard
import pyautogui
import pywinctl as pwc
import websockets
from log import setupLogger
from environment import global_environ

logger = setupLogger(__file__)
targetUrl = global_environ

class NotSupportPlatform(Exception):
    pass

def detect_system():
    p = platform.system().lower()
    if p == "darwin":
        return "MacOs"
    elif p == "win32":
        return "Windows"
    else:
        raise NotSupportPlatform()

current_system = detect_system()
if current_system == "Windows":
    combination = "ctrl+shift+J"
    detect_window_title = "Microsoft​ Edge"
elif current_system == "MacOs":
    combination = "command+j"
    detect_window_title = "Google Chrome"

def on_hotkey_press():
    try:
        logger.info(f"Key combination '{combination}' was pressed.")
        logger.info(f"Detecting window: {detect_window_title}")
        window = findWindow(detect_window_title)
        logger.info(f"Find a window: {window}")
        if window is None:
            logger.warning("Window can be not fojund")
            return
        window.activate()
        asyncio.run(activate_tab())
    except Exception as e:
        logger.error("Run into error", exc_info=e)

keyboard.add_hotkey(combination, on_hotkey_press)

connected_clients = set()
queue = []


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
        except asyncio.exceptions.TimeoutError as e:
            pass
        except Exception as e:
            logger.error("Accept an unexpected error", exc_info=e)

async def send(websocket, message):
    payload = json.dumps(message)
    logger.info(f"Sending message to clients: {payload}")
    await websocket.send(payload)

async def activate_tab():
    message = {"action": "activateTab", "tabUrl": targetUrl}
    logger.info("Add a new message to the queue")
    queue.append(message)


def findWindow(keyword: str):
    pyautogui.press("alt")
    allWindows = pwc.getAllWindows()
    for window in allWindows:
        logger.debug(window)
        if isinstance(window.title, str) and keyword.lower() in window.title.lower():
            return window
    return None

start_server = websockets.serve(handle_websocket, "localhost", 8080)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()