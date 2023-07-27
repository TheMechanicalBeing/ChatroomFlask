from mainContent import app, bcrypt, db
from flask import render_template, flash, redirect, url_for
from mainContent.forms import RegistrationForm, LoginForm
from mainContent.models import User


@app.route('/')
@app.route('/home')
def home():
    return render_template('mainpage.html', title='Home')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name=form.first_name.data.capitalize(), last_name=form.last_name.data.capitalize(),
                    username=form.username.data, age=form.age.data, password=hashed_password, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Account logged in successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('login.html', title='Login', form=form)
