# main.py - FastAPI backend for Gin Rummy with rooms

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List, Dict

app = FastAPI()

# Dictionary to keep track of rooms and connected clients
rooms: Dict[str, List[WebSocket]] = {}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    room_name = None
    player_name = None

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            if message["type"] == "join":
                room_name = message["room"]
                player_name = message.get("player", "Anonymous")

                if room_name not in rooms:
                    rooms[room_name] = []
                rooms[room_name].append(websocket)

                # Notify all players in the room
                await broadcast_room(
                    room_name,
                    {"type": "game-update", "payload": f"{player_name} joined the room!"}
                )

            elif message["type"] == "game-action":
                # Broadcast the action to all players in the room
                if room_name:
                    await broadcast_room(
                        room_name,
                        {
                            "type": "game-update",
                            "payload": {"player": player_name, "action": message["payload"]}
                        }
                    )

    except WebSocketDisconnect:
        if room_name and websocket in rooms.get(room_name, []):
            rooms[room_name].remove(websocket)
            await broadcast_room(
                room_name,
                {"type": "game-update", "payload": f"{player_name} left the room."}
            )

import json

async def broadcast_room(room_name: str, message: dict):
    """Send a message to all clients in a room"""
    if room_name in rooms:
        for client in rooms[room_name]:
            try:
                await client.send_text(json.dumps(message))
            except:
                pass  # Ignore disconnected clients
