from flask import render_template
from flask_login import login_required, current_user

from app import app


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/create_room')
def create_room_page():
    return render_template("create_room.html")


@app.route('/login')
def login_page():
    return render_template("login.html")


@app.route('/statistics')
@login_required
def statistics_page():
    return render_template("statistics.html", name=current_user.name)
