import sys
import os
import random

from flask import Flask, render_template, request
from flask_socketio import SocketIO

top_level_dir = os.path.abspath('../')
sys.path.append(top_level_dir)

from trivia_generator.web_scraper.WebScraper import get_page_by_random
from trivia_generator.NLPPreProcessor import create_TUnits
from database_connection.dbconn import DBConn


app = Flask(__name__)
socketio = SocketIO(app)

tunit_dictionary = dict()

dbconn = DBConn()


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@socketio.on('update_rank')
def update_rank(rank):
    try:
        tunit = tunit_dictionary[request.sid]
        if rank == 'like':
            tunit.num_likes += 1
        elif rank == 'dislike':
            tunit.num_dislikes += 1
        elif rank == 'meh':
            tunit.num_mehs += 1
        else:
            print("invalid rank submitted")
        # update tunit in database
        dbconn.update_tunit(tunit)
    except KeyError:
        print("could not find SID")


@socketio.on('request_trivia')
def request_trivia(info):
    trivia_article = get_page_by_random()
    tunit_list = create_TUnits(trivia_article)
    while not tunit_list:
        print("bad article!")
        trivia_article = get_page_by_random()
        tunit_list = create_TUnits(trivia_article)
    trivia = random.choice(tunit_list)
    tunit_dictionary[request.sid] = trivia
    return trivia.sentence


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
