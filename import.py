from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *
import csv, os

app = Flask(__name__)

engine = create_engine(os.getenv("DATABASE_URL"))
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

def main():
    # check if tables aleardy exist
    if not engine.dialect.has_table(engine, 'books'):
        print('DB is empty! \nCreating tables...')
        db.create_all()
        print('Done.')

    # import data
    file = open('books.csv')
    reader = csv.reader(file)
    i = 0
    for isbn, title, author, year in reader:
        if i==0:
            i += 1
            continue
        book = Book(isbn=isbn, title=title, author=author, year=year)
        db.session.add(book)
        print(f'Added book {title} with isbn {isbn}')
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        print('Entered main program.')
        main()
