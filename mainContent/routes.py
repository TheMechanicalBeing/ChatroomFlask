from mainContent import app
from flask import render_template
from mainContent.forms import RegistrationForm, LoginForm


@app.route('/')
def home():
    return render_template('mainpage.html', title='Home')


@app.route('/register')
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Register', form=form)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)
