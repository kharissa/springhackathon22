from bahay import app, db, bcrypt
from flask import render_template, url_for, flash, redirect, request, jsonify
from bahay.models import User, House, Room, Task, History
from bahay.forms import AddRoomForm, AddTaskForm, RegistrationForm, LoginForm, JoinForm, CreateForm
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime, timedelta

@app.route("/")
def home():
    """ Render Home page. """
    return render_template("home.html")

@app.route("/profile")
def profile():
    """ Render Profile page. """
    return render_template("account/profile.html")

@app.route("/history")
def history():
    """ Render History page. """
    return render_template("account/history.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """ Render User Registration form. """
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed_password, first_name=form.first_name.data, last_name=form.last_name.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(f"Welcome to Bahay, {user.first_name}! You are now logged in.", "success")
        return redirect(url_for("profile"))
    return render_template("account/register.html", title="Registration", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    """ Render User Login form. """
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f"Welcome back, {user.first_name}", "success")
            return redirect(url_for("profile"))
        else:
            flash("Login Unsuccessful. Please check email and password and try again.", "danger")
    return render_template("account/login.html", title="Login", form=form)

@app.route("/logout")
def logout():
    """ Logs out user. """
    logout_user()
    return redirect(url_for("home"))

@app.route("/house", methods=["GET", "POST"])
def create_house():
    """ Render Create a House form. """
    form = CreateForm()
    if form.validate_on_submit():
        house = House(name=form.name.data, code=form.code.data)
        db.session.add(house)
        current_user.house = house
        db.session.commit()
        flash("Great! Next step is to share your join code with your roommates.", "success")
        return redirect(url_for("profile"))
    return render_template("house/create.html", title="Create a House", form=form)

@app.route("/house/join", methods=["GET", "POST"])
def join_house():
    """ Render Join a House form. """
    form = JoinForm()
    if form.validate_on_submit():
        house = House.query.filter_by(code=form.code.data).first()
        current_user.house = house
        db.session.commit()
        if house:
            flash("Awesome! You just joined a house. Start winning points!", "success")
            return redirect(url_for("profile"))
        flash("Incorrect join code given. Please check and try again.", "danger")
    return render_template("house/join.html", title="Join a House", form=form)

@app.route("/room", methods=["GET", "POST"])
def add_room():
    """ Render Add a Room form. """
    form = AddRoomForm()
    if form.validate_on_submit():
        room = Room(name=form.name.data, house=current_user.house)
        db.session.add(room)
        db.session.commit()
        return redirect(url_for("profile"))
    return render_template("house/add-room.html", title="Add a Room", form=form)

@app.route("/task", methods=["GET", "POST"])
def add_task():
    """ Render Add a Task form. """
    form = AddTaskForm()
    if form.validate_on_submit():
        room = Room.query.get(request.args['id'])
        due_date = datetime.utcnow() + timedelta(days=form.frequency.data)
        task = Task(name=form.name.data, frequency=form.frequency.data, points=form.points.data, room=room, room_id=room.id, due_date=due_date)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for("profile"))
    return render_template("house/add-task.html", title="Add a Task", form=form)

@app.route("/task/done", methods=["GET", "POST"])
def done_task():
    """ Add a completed task to UserTasks. """
    if request.args:
        # Change due date of task
        task = Task.query.get(request.args['id'])
        task.due_date = datetime.utcnow() + timedelta(days=task.frequency)

        # Create task history
        history = History(user_id=current_user.id, task_id=request.args['id'])
        db.session.add(history)

        # Add points to user
        current_user.points += task.points
        db.session.commit()

        return redirect(request.referrer)

@app.route("/history/all", methods=["GET", "POST"])
def get_history():
    history = History.query.all()
    return jsonify([
        {'id': hist.id, 'done_at': hist.done_at, 'user_id': hist.user_id, 'task_id': hist.task_id, 'task': hist.task.name, 'user': hist.user.first_name} for hist in history]
    )