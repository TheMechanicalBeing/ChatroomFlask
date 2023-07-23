from mainContent import app
from flask import render_template, flash, redirect, url_for
from mainContent.forms import RegistrationForm, LoginForm


@app.route('/')
@app.route('/home')
def home():
    return render_template('mainpage.html', title='Home')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
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
