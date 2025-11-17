import socketio

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
app = socketio.ASGIApp(sio)


def chat_room_for_users(user1_id, user2_id):
    a, b = sorted([user1_id, user2_id])
    return f"chat_{a}_{b}"


@sio.event
async def connect(sid, environ):
    print("Client connected:", sid)


@sio.event
async def disconnect(sid):
    print("Client disconnected:", sid)


@sio.event
async def join_chat(sid, data):
    room = chat_room_for_users(data["current_user_id"], data["other_user_id"])
    sio.enter_room(sid, room)
    print(f"{sid} joined {room}")


@sio.event
async def send_chat_message(sid, data):
    """
    data = {
        "room": "chat_1_2",
        "sender_username": "...",
        "text": "..."
    }
    """
    room = data["room"]
    await sio.emit("new_chat_message", data, room=room)
