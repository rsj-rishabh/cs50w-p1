import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from models import *

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
# engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))
db.init_app(app)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/register")
def go_to_register():
    return render_template('register.html')


@app.route("/registration_status", methods=['POST'])
def register():
    id = request.form.get('user_id')
    name = request.form.get('name')
    passcode = request.form.get('passcode')
    user = User(id=id, name=name, passcode=passcode)
    
    db.session.add(user)
    return render_template('index.html')
