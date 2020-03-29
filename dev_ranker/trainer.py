import sys
import os
import random

from flask import Flask, render_template
from flask_socketio import SocketIO

top_level_dir = os.path.abspath('../')
sys.path.append(top_level_dir)

from trivia_generator.web_scraper.WebScraper import get_page_by_random
from trivia_generator.NLPPreProcessor import create_TUnits


app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@socketio.on('update_rank')
def update_rank(rank):
    if rank == 'like':
        pass
    elif rank == 'dislike':
        pass
    elif rank == 'meh':
        pass
    else:
        pass


@socketio.on('request_trivia')
def request_trivia(info):
    trivia_article = get_page_by_random()
    tunit_list = create_TUnits(trivia_article)
    trivia = None
    for tunit in tunit_list:
        if is_interesting(tunit):
            trivia = tunit.sentence
            print('interesting trivia!!!')
            break
    if trivia is None:
        trivia = random.choice(tunit_list)
        print('uninteresting trivia...')
    return trivia.sentence


def is_interesting(tunit):
    return (tunit.has_superlative or
            tunit.has_contrasting)


if __name__ == '__main__':
    socketio.run(app)
