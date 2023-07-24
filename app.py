from mainContent import app, db
from mainContent.models import User, Room, Message
# from flask_bcrypt import Bcrypt
# from mainContent import socketio

with app.app_context():
    db.create_all()
