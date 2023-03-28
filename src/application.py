from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from helpers import get_vocab_list
from flask import Flask, flash, jsonify, redirect, render_template, request, session
# from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
from enum import Enum
# from tempfile import mkdtemp
# from cs50 import SQL
# import os
# import time

# Configure application

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
# app.config['SECRET_KEY'] = 'secret!'
app.secret_key = 'bruh'

socketio = SocketIO(app)

# Dictionary in the form { room_id : frequency } where frequency is the number of players in the room
# form { room_id : passage }
# form { room_id : number of completed passages }


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)

# app.config["SESSION_FILE_DIR"] = mkdtemp()
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)


# db = SQL(os.environ.get("DATABASE_URL")) # replace "DATABASE_URL" with the actual PostgreSQL URL

"""
Vision:
Home page is a language selection, just going to be a drop-down menu. After selecting a language, you are taken to a page with tiles
representing each unit (like typesprinter), each unit has a picture on it representing the general vocab/grammar. Along the top of the
unit pages, there will be a banner containing links to: (1) go back to the unit selection page, (2) go to unit vocab list, (3) view unit
grammar, (4) go to unit conversation chatbot (5) previous/next unit arrows, (6) unit flash cards, (7) cross-language dictionary.
Mockup banner shown below.

< UNIT i - 1     VIEW ALL UNITS   DICTIONARY   VOCAB   GRAMMAR   FLASH CARDS   CONVERSE     UNIT i + 1 >


General app structure in mind:

/           ->  language selection
/unitselect ->  unit selection
/unit<i>    ->  ith unit, one route per unit. most likely unit<i>_<language> (POTENTIALLY JUST USE /vocab INSTEAD)
/vocab      ->  vocab list for the unit (only one route needed, populate with vocab list passed in through the backend)
/grammar    ->  unit grammar page, likely just a scrollable/paged route with no input
/dictionary ->  cross-language searchable dictionary (searchable by user's native language)
/cards      ->  flash cards
/converse   ->  chat bots

"""

# Session vars

# native_language
# target_language
# unit
# unit_names


# Global Vars

unit_names = {
    'english' : ['Greetings', 'Restaurant', 'Weather', 'Doctor\'s Office'],
    'russian' : ['Приветствия', 'В Ресторане', 'Погода', 'Офис Врача']
}

nav_tabs = {
    'english' : ['All Units', 'Dictionary', 'Vocab', 'Grammar', 'Flash Cards', 'Converse'],
    'russian' : ['Все Урокы', 'Словарь', 'Словарный Запас', 'Грамматика', 'Флешки', 'Говирить']
}

chat = {
    'english' : 'Let\'s Talk!',
    'russian' : 'Давайте Поговорим!'
}



@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    # language = <INSERT LANGUAGE BASED ON WHAT THEY CHOOSE> # possibly under a different route

    session['native_language'] = request.form.get('native_language')
    session['target_language'] = request.form.get('target_language')

    session['unit_names'] = unit_names[session['native_language']]
    session['nav_tabs'] = nav_tabs[session['native_language']]

    return redirect("/unitselect")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/deliverables")
def deliverables():
    return render_template("deliverable_select.html")
    

@app.route("/unitselect", methods=['GET', 'POST'])
def unit_selection():
    if request.method == 'GET':
        return render_template("unit_select.html", unit_names=session['unit_names'], nav_tabs=session['nav_tabs'])
    
    session['unit'] = request.form.get('unit_num')


@app.route("/unit1", methods=['GET', 'POST'])
def unit1():
    session['unit'] = 1
    unit_language = "unit1_" + session['target_language'] + ".html"
    print(unit_language)

    return render_template(unit_language, unit_names=session['unit_names'], nav_tabs=session['nav_tabs'])


@app.route("/unit2", methods=['GET', 'POST'])
def unit2():
    session['unit'] = 2
    unit_language = "unit2_" + session['target_language'] + ".html"

    return render_template(unit_language, unit_names=session['unit_names'], nav_tabs=session['nav_tabs'])


@app.route("/grammar")
def grammar():
    grammar_unit = "unit" + str(session['unit']) + "_grammar_" + session['target_language'] + ".html"

    return render_template(grammar_unit, unit_names=session['unit_names'], nav_tabs=session['nav_tabs'])


@app.route("/dictionary")
def dictionary():
    dictionary_language = session['native_language'] + "_" + session['target_language'] + "_dictionary.html"

    return render_template(dictionary_language, unit_names=session['unit_names'], nav_tabs=session['nav_tabs'])


@app.route("/cards")
def flash_cards():
    random_text = "unit" + str(session['unit']) + ".json"

    return render_template("flashcards.html", random_text=random_text, unit_names=session['unit_names'], nav_tabs=session['nav_tabs'])


@app.route("/chat")
def converse():
    # load unit-specific chat bot

    return render_template("chat.html", unit_names=session['unit_names'], nav_tabs=session['nav_tabs'], chat=chat[session['target_language']])





# Old typesprinter routes, for reference only

"""
@app.route("/verify", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "GET":
        return render_template("verify.html")

    # You really thought I was gonna hard-code a non-hashed password?
    if(check_password_hash("pbkdf2:sha256:150000$Yd7q1JuY$06aeeb26761c11fa8ebf687f493207bd18cbf0be42fd567fbe35215c1ed42bd0", request.form.get("password"))):
        session["user_id"] = "admin"
        return redirect("/admin")

    return redirect("/")


@app.route("/admin", methods=["GET", "POST"])
@login_required
def race():
    session.pop("commands", None)
    session.pop("passage", None)

    if request.method == "GET":
        return render_template("commands.html")

    commands = request.form.get("commands")
    index = commands.rfind(" ")

    if index > 0 and commands[index-4:index] == "room":
        session["room-commands"] = commands[index + 1:]
        session["commands"] = commands

    return redirect("/1v1")


@socketio.on('join', namespace='/test')
def join(message):
    print('Joined room ' + message['room'])
    join_room(message['room'])

    # Gets room frequency, returns 0 if not found
    freq = room_list.get(message['room'], 0) # https://github.com/miguelgrinberg/Flask-SocketIO/issues/105

    if freq == 0:
        room_list[message['room']] = 1
        try:
            room_passage[message['room']] = session["passage"]
        except:
            room_passage[message['room']] = pick_passage()
    else:
        room_list[message['room']] += 1

    emit('join_lobby', {
        'players' : room_list[message['room']],
        'passage' : room_passage[message['room']],
        'room' : message['room']
    }, room=message['room'])

    if not freq == 0:
        emit('update_countdown', {
            'timer' : COUNTDOWN,
            'room' : message['room']
        }, room=message['room'])

    session['receive_count'] = session.get('receive_count', 0) + 1


@socketio.on('leave', namespace='/test')
def leave(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1


@socketio.on('race finished', namespace='/test')
def rank(message):
    finished = room_finish.get(message['room'], 0)

    if finished == 0:
        room_finish[message['room']] = 1
    else:
        room_finish[message['room']] += 1

    # taken from https://stackoverflow.com/questions/9647202/ordinal-numbers-replacement
    ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])

    emit('end_message', {
        'place' : ordinal(room_finish[message['room']])
    })

    if room_finish[message['room']] == room_list[message['room']]:
        room_list.pop(message['room'], None)
        room_passage.pop(message['room'], None)
        room_finish.pop(message['room'], None)

        if message['room'] == session["room-commands"]:
            session.pop("commands")
            session.pop("room-commands")

"""


if __name__ == '__main__':
    socketio.run(app, debug=True)