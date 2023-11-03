from mainContent import app, bcrypt, db, select_command
from flask import render_template, flash, redirect, url_for, request, session, g
from mainContent.forms import RegistrationForm, LoginForm, UpdateAccountForm
from mainContent.models import User, Room, user_room
from sqlalchemy import text
import secrets
import os
from PIL import Image
import functools


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        with app.app_context():
            load_logged_in_user()
            if g.get("user", None) is None:
                return redirect(url_for("login"))

        return view(**kwargs)

    return wrapped_view


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        create = request.form.get('create', False)
        join = request.form.get('join', False)
        request_code = request.form.get('code')

        if create is not False:
            new_room = Room(code=secrets.token_hex(8))
            db.session.add(new_room)
            # Usage of current user
            g.user.rooms.append(new_room)
            db.session.commit()
            return redirect(url_for('room', code=new_room.code))

        elif join is not False:

            if request_code is None:
                flash('The input field should not be empty when trying to join the room.')

            elif not select_command("room", {"code": request_code}).first():
                flash('The given code does not exist.')
                return redirect(url_for('home'))

            else:
                if not select_command("user_room", {"user_id": g.user.id}).first():
                    g.user.rooms.append(Room.query.filter_by(code=request_code).first())
                    db.session.commit()
                session["current_room_code"] = request_code
                return redirect(url_for('room', code=request_code))

    return render_template('mainpage.html', title='Home')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if g.user:
        return redirect(url_for('home'))
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
    if g.user:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # Login User
            session.clear()
            session["user_id"] = user.id
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password if it is written correct.')

    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            g.user.image_file = picture_file
        g.user.first_name = form.first_name.data
        g.user.last_name = form.last_name.data
        g.user.age = form.age.data
        g.user.username = form.username.data
        g.user.email = form.email.data
        db.session.commit()
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.first_name.data = g.user.first_name
        form.last_name.data = g.user.last_name
        form.age.data = g.user.age
        form.username.data = g.user.username
        form.email.data = g.user.email
    image_file = url_for('static', filename='profile_pics/' + g.user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route('/room/<string:code>', methods=['GET', 'POST'])
@login_required
def room(code):
    if not db.session.execute(text("SELECT code FROM room WHERE code = '{}'".format(code))).first():
        flash("The given code does not exist or you don't have access to join this room.")
        return redirect(url_for("home"))
    return render_template('room.html', title='Room', code=code)


@app.before_request
def load_logged_in_user():
    user_id = session.get("user_id", None)

    if user_id is None:
        g.user = None
    else:
        g.user = db.session.execute(
            text("SELECT * FROM user WHERE id = {}".format(user_id))
        ).fetchone()
