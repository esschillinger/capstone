from flask_socketio import SocketIO, emit
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from googletrans import Translator
from random import randrange
import openai
# from werkzeug.security import check_password_hash, generate_password_hash
# from flask_session import Session
# from tempfile import mkdtemp
# from cs50 import SQL
# import os
# import time

# Configure application

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SECRET_KEY'] = 'bruh'

socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")


ts = Translator()

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

nav_unit_tabs = {
    'english' : ['All Units', 'Dictionary', 'Vocab', 'Exercises', 'Flash Cards', 'Converse'],
    'russian' : ['Все Урокы', 'Словарь', 'Словарный Запас', 'Упражнение', 'Флешки', 'Говирить']
}

nav_home_tabs = {
    'english' : ['Home', 'About'],
    'russian' : ['Дом', 'О нас']
}

chat = {
    'english' : 'Let\'s Talk!',
    'russian' : 'Давайте Поговорим!'
}

prompts = {
    'english' : [''],
    'russian' : [''],
}



@app.route("/", methods=['GET', 'POST'])
def index():
    if 'nav_home_tabs' not in session: # app just launched
        session['nav_home_tabs'] = nav_home_tabs['english']

    if request.method == 'GET':
        return render_template('index.html', nav_tabs=session['nav_home_tabs'])

    session['native_language'] = request.form.get('native_language')
    session['target_language'] = request.form.get('target_language')

    session['unit_names'] = unit_names[session['native_language']]
    session['nav_home_tabs'] = nav_home_tabs[session['native_language']]
    session['nav_unit_tabs'] = nav_unit_tabs[session['native_language']]

    return redirect("/unitselect")


@app.route("/about")
def about():
    return render_template("about.html", nav_tabs=session['nav_home_tabs'])


@app.route("/unitselect", methods=['GET', 'POST'])
def unit_selection():
    if request.method == 'GET':
        return render_template("unit_select.html", unit_names=session['unit_names'], nav_tabs=session['nav_home_tabs'])
    
    session['unit'] = request.form.get('unit_num')


@app.route("/unit1", methods=['GET', 'POST'])
def unit1():
    session['unit'] = 1
    unit_language = "unit1_" + session['target_language'] + ".html"
    print(unit_language)

    return render_template(unit_language, unit_names=session['unit_names'], nav_tabs=session['nav_unit_tabs'])


@app.route("/unit2", methods=['GET', 'POST'])
def unit2():
    session['unit'] = 2
    unit_language = "unit2_" + session['target_language'] + ".html"

    return render_template(unit_language, unit_names=session['unit_names'], nav_tabs=session['nav_unit_tabs'])


@app.route("/unit3", methods=['GET', 'POST'])
def unit3():
    session['unit'] = 3
    unit_language = "unit3_" + session['target_language'] + ".html"

    return render_template(unit_language, unit_names=session['unit_names'], nav_tabs=session['nav_unit_tabs'])


@app.route("/grammar")
def grammar():
    return render_template("grammar.html")


@app.route("/exercises")
def exercises():
    unit = "unit" + str(session['unit']) + ".json"

    return render_template("quiz.html", unit=unit, unit_names=session['unit_names'], nav_tabs=session['nav_unit_tabs'])


@app.route("/dictionary")
def dictionary():
    unit = "unit" + str(session['unit']) + ".json"

    return render_template("dictionary.html", unit = unit, unit_names=session['unit_names'], nav_tabs=session['nav_unit_tabs'])

@app.route("/vocab")
def vocab():
    unit = "unit" + str(session['unit']) + ".json"

    return render_template("vocab.html", unit = unit, unit_names=session['unit_names'], nav_tabs=session['nav_unit_tabs'])

@app.route("/cards")
def flash_cards():
    unit = "unit" + str(session['unit']) + ".json"

    return render_template("flashcards.html", unit=unit, unit_names=session['unit_names'], nav_tabs=session['nav_unit_tabs'])


@app.route("/chat")
def converse():
    # load unit-specific chat bot
    #key is on my desktop in PASSCODES.txt file

    with open('C:\\Users\\eschillinger\\Desktop\\PASSCODE.txt') as f:
        lines = f.readlines()
        key = lines[0].strip()

    openai.api_key = key

    session['prompt'] =  """AT NO POINT RESPOND IN ANYTHING ASIDE FROM RUSSIAN WITH THIS PROMPT, DO NOT TRANSLATE, AND DO NOT ELABORATE ON WHAT YOU MEANT. You are a russian teacher for a second grade class who only speaks in russian who is holding a conversation on TOPIC for a grade with a student. Only take the role of the strict teacher. Never use english and do not provide translations. The student respond with a sentence or two, if they do not respond in Russian, please respond with \"Пожалуйста, говорите по-русски.\" and then repeat the previous prompt. Do not count this as an exchange. Please respond to the student with a sentence or two within the context of what you are testing them on. Only speak in russian and never at any point translate anything to english or include the english meaning."""
    session['prompt'] = session['prompt'].replace("TOPIC", "[" + unit_names['english'][session['unit'] - 1] + "]")

    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo", # The deployment name you chose when you deployed the ChatGPT or GPT-4 model.
        messages = [
            {
                "role" : "system",
                "content" : session['prompt']
            },
            {
                "role" : "user",
                "content" : ""
            },
        ]
    )
    first_message = response.choices[0].message.content

    return render_template("chat.html", unit_names=session['unit_names'], nav_tabs=session['nav_unit_tabs'], chat=chat[session['target_language']], first_message=first_message)


# Websockets

@socketio.on('join', namespace='/gpt')
def prompt_gpt():
    # prompt GPT API when the chat page is loaded (maybe only do this on the first message sent to save tokens?)
    # TODO

    print('User joined \'/chat\'.')


@socketio.on('leave', namespace='/gpt')
def reset_gpt():
    # maybe you need to clear the API here when the user leaves the chat page to start fresh
    # Probably not though because GPT will be re-prompted when 'join' is emitted
    # TODO

    print('User left \'/chat\'.')


@socketio.on('user_message', namespace='/gpt') # maybe need a namespace field here?
def user_message(message):
    # when the user sends a message
    # pass to C-GPT API
    # receive response
    # emit response and grade
    # note: 'message' is a dictionary containing the user message under the field 'data'
    # TODO

    # user message stored in message['data']
    session['prompt'] += message['data'] + '\n\n'

    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {
                "role" : "system",
                "content" : session['prompt']
            },
            {
                "role" : "user",
                "content" : message['data']
            },
        ]
    )
    reply = response.choices[0].message.content

    # format = (VocabGrade, GrammarGrade, SpellingGrade, RelevanceGrade, explanation)
    grades = gradeResponse(message['data'])

    emit('ai_response', {
        'data' : reply,
        'translation' : ts.translate(reply, src=session['target_language'][:2], dest=session['native_language'][:2]).text,
        'grade_msg' : grades[4],
        'spelling' : grades[2],
        'grammar' : grades[1],
        'vocab' : grades[0],
        'revelance' : grades[3]
    })





def gradeResponse(user_input):
    #ask the system to grade the user
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {
                "role" : "system",
                "content" : "Please explicitly grade the student's performance out of 10. Explicitly state each of the 4 subscores (Vocabulary, Grammar, Spelling, Relevance to the topic) for the response each out of 10 as well. Then explain why you gave them that score."
            },
            {
                "role" : "user",
                "content" : user_input
            },
        ]
    )

    #output the grade (debugging tool)
    #print(response.choices[0].message.content)

    #parse the grade response for the scores of vocab, grammar, spelling, and relevance int VocabGrade, GrammarGrade, SpellingGrade, and RelevanceGrade

    #get the grade
    grade = response.choices[0].message.content

    #get the vocab grade
    VocabGrade = grade[grade.find("Vocabulary: ") + 12]
    VocabGrade += grade[grade.find("Vocabulary: ") + 13]
    #if VocabGrade has a / in it then delete it
    if VocabGrade.find("/") != -1:
        VocabGrade = VocabGrade[0]

    #get the grammar grade
    GrammarGrade = grade[grade.find("Grammar: ") + 9]
    GrammarGrade += grade[grade.find("Grammar: ") + 10]
    #if GrammarGrade has a / in it then delete it
    if GrammarGrade.find("/") != -1:
        GrammarGrade = GrammarGrade[0]

    #get the spelling grade
    SpellingGrade = grade[grade.find("Spelling: ") + 10]
    SpellingGrade += grade[grade.find("Spelling: ") + 11]
    #if SpellingGrade has a / in it then delete it
    if SpellingGrade.find("/") != -1:
        SpellingGrade = SpellingGrade[0]

    #get the relevance grade
    RelevanceGrade = grade[grade.find("Relevance to the topic: ") + 24]
    RelevanceGrade += grade[grade.find("Relevance to the topic: ") + 25]
    #if RelevanceGrade has a / in it then delete it
    if RelevanceGrade.find("/") != -1:
        RelevanceGrade = RelevanceGrade[0]

    #get everything from "Exlpaination: " to the end of the string and store it in explanation
    explanation = grade[grade.find("Relevance to the topic: ") + 28:]
    
    return VocabGrade, GrammarGrade, SpellingGrade, RelevanceGrade, explanation


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