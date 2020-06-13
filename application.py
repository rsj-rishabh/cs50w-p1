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

@app.route("/")
def index():
    return render_template('index.html', message='')

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
