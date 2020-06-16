# for getting path variables
import os

# for flask operations
from flask import Flask, session, render_template, request
from flask_session import Session

# for database operations
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from models import *

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Set up session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

session_user = {}

@app.route("/")
def index():
    print( f"{session_user} from Index" )
    if session_user == {}:
        return render_template('index.html', message='')
    else:
        return render_template('home.html', name=session_user['name'])

@app.route("/register")
def go_to_register():
    return render_template('register.html')

@app.route("/registration_status", methods=['POST'])
def register():
    id = request.form.get('user_id')
    name = request.form.get('name')
    passcode = request.form.get('passcode')
    user = User(id=id, name=name, passcode=passcode)
    try:
        db.session.add(user)
        print(f'User {id} added to the database.')
        db.session.commit()
        return render_template('index.html', message=f'Welcome {name} to the Book-o-holics fam!')
    except:
        return render_template('index.html', message=f'Alas! The user with ID {id} already exists.')

@app.route("/login")
def go_to_login():
    print( f"{session_user} from go_to_login" )
    if session_user=={}:
        return render_template('login.html', message='')
    else:
        return render_template('home.html', name=session_user['name'])

@app.route("/logout")
def logout():
    session_user.pop('user')
    session_user.pop('name')
    print( f"{session_user} from logout" )
    return render_template('logout.html')

@app.route("/home", methods=['POST','GET'])
def login():
    if request.method == "POST":
        id = request.form.get('user_id')
        passcode = request.form.get('passcode')
        user = User.query.get(id)
        if user is None:
            return render_template('login.html', message='No such user exists.')
        else:
            if user.passcode == passcode:
                session_user.update({'user':id, 'name':user.name})
                print( f"{session_user} from Login POST" )
                return render_template('home.html', name=session_user['name'])
            else:
                return render_template('login.html', message='Invalid user id / passcode.')
    else:
        print( f"{session_user} from Login GET" )
        if session_user=={}:
            return render_template('index.html', message='Please login to enter home.')
        else:
            return render_template('home.html', name=session_user['name'])
