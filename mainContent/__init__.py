from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ad9b54de1f816dc820904f67a2b4c6b8de8d6654d645bce38faf6836855e2a41'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
with app.app_context():
    db = SQLAlchemy(app)
    bcrypt = Bcrypt(app)


from mainContent import routes
