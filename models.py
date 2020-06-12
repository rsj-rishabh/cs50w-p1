from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    __tablename__ = 'books'
    isbn = db.Column( db.String, primary_key=True )
    title = db.Column( db.String, nullable=False )
    author = db.Column( db.String, nullable=False )
    year = db.Column( db.String, nullable=False )

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column( db.String, primary_key=True )
    name = db.Column( db.String,  nullable=False)
    passcode = db.Column( db.String, nullable=False )

class Reviews(db.Model):
    __tablename__ = 'reviews'
    id = db.Column( db.String, primary_key=True )
    book_id = db.Column( db.String, db.ForeignKey('books.isbn'), nullable=False )
    user_id = db.Column( db.String, db.ForeignKey('users.id'), nullable=False )
    review = db.Column( db.String, nullable=False )
