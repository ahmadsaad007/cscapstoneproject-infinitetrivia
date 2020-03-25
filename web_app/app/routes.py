from flask import render_template

from app import app


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/create_room')
def create_room_page():
    return render_template("create_room.html")
