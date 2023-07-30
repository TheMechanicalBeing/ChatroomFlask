from mainContent import app, bcrypt, db
from flask import render_template, flash, redirect, url_for, request
from mainContent.forms import RegistrationForm, LoginForm, UpdateAccountForm
from mainContent.models import User, Room, user_room
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from PIL import Image


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        create = request.form.get('create', False)
        join = request.form.get('join', False)
        request_code = request.form.get('user_code')

        if create is not False:
            new_room = Room(code=secrets.token_hex(8))
            db.session.add(new_room)
            current_user.rooms.append(new_room)
            db.session.commit()
            return redirect(url_for('room', code=new_room.code))
        elif join is not False:
            if not db.session.execute(db.Select(Room).filter_by(code=request_code)).first():
                flash('The given code does not exist.')
                return redirect(url_for('home'))
            else:
                if not user_room.query.filter_by(user_id=current_user.id).first():
                    current_user.rooms.append(Room.query.filter_by(code=request_code).first()[0])
                    db.session.commit()
                return redirect(url_for('room', code=request_code))

    return render_template('mainpage.html', title='Home')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password if it is written correct.')

    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
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
            current_user.image_file = picture_file
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.age = form.age.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.age.data = current_user.age
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route('/room/<string:code>', methods=['GET', 'POST'])
@login_required
def room(code):
    return render_template('room.html', title='Room')

