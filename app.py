from mainContent import app, db
from mainContent.models import User, Room, Message


with app.app_context():
    db.create_all()
