from flaskChat import app, db
from flaskChat.models import User, Room
from flask_bcrypt import Bcrypt
from flaskChat import socketio


with app.app_context():
    db.create_all()


if __name__ == '__main__':
    db.create_all()
