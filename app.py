from mainContent import app, db
from mainContent.models import User, Room, Message
import time
from flask import session


if __name__ == "__main__":
    app.run(debug=True)
    while(True):
        with app.app_context():
            print(f"g is {session}")
            time.sleep(5)
