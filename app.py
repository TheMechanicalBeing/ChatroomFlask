from mainContent import app, db, socketio
from mainContent.models import User, Room, Message


if __name__ == "__main__":
    socketio.run(app, debug=True)
