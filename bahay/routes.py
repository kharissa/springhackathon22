from bahay import app
from flask import render_template

@app.route("/")
def home():
    """ Render Home page. """
    return render_template("home.html")

