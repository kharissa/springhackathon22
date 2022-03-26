from bahay import app
from flask import render_template
from bahay.models import User, House, Room, Task

@app.route("/")
def home():
    """ Render Home page. """
    return render_template("home.html")


@app.route("/login")
def login():
    """ Render Login page. """
    return render_template("login.html")


@app.route("/register")
def register():
    """ Render Register page. """
    return render_template("register.html")
