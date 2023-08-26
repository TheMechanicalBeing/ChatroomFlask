from . import socketio, select_command
from flask import session
from flask_login import current_user
from flask_socketio import join_room, leave_room, send


@socketio.on("connect")
def connect(auth):
    print("tornike joined the room")


@socketio.on("disconnect")
def disconnect():
    print("tornike left the room")
