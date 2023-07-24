from mainContent import db
from datetime import datetime


user_room = db.Table(
    "user_room",
    db.Column('user_id', db.ForeignKey('user.id'), primary_key=True),
    db.Column('room_id', db.ForeignKey('room.id'), primary_key=True)
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    age = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    image_file = db.Column(db.String, nullable=False, default='default.jpg')
    rooms = db.Relationship('Room', secondary=user_room, backref='user')
    messages = db.Relationship('Message', backref='user', lazy=True)

    def __repr__(self):
        return f'User - {self.username}, {self.email}, {self.image_file}'


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String, nullable=False, unique=True)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    users = db.Relationship('User', secondary=user_room, backref='room')
    messages = db.Relationship('Message', backref='room', lazy=True)

    def __repr__(self):
        return f'Room - {self.code}, {self.creation_date}'


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    message_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)

    def __repr__(self):
        return f'Message - {self.message_date}, {self.content}'
