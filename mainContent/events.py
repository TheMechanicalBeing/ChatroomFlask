from flask_socketio import SocketIO

socketio = SocketIO()


@socketio.on("connect")
def handle_connect():
    print("Client Connected!")


@socketio.on("user_join")
def handle_user_join(username):
    print(f"Hello, {username}")
