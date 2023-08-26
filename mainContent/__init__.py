from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO
from sqlalchemy import text


def select_command(table_name, params, select="*"):
    command = "SELECT {} FROM {}".format(select, table_name)
    if params is not None:
        command += " WHERE"
        for key, value in params.items():
            command += " {}=:param".format(key)
            return db.session.execute(text(command), {"param": value})


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ad9b54de1f816dc820904f67a2b4c6b8de8d6654d645bce38faf6836855e2a41'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
with app.app_context():
    db = SQLAlchemy(app)
    bcrypt = Bcrypt(app)
    login_manager = LoginManager(app)
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'
    socketio = SocketIO(app)


from mainContent import routes
