#This is the imports
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func



#This is for all the comments on the sections
class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(10000))
    description = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone = True), default = func.now())
    #Foreign key things
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#This is the eventinfo table
class EventInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    #Foreign key things
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#This is the user table / this is the schema / layout of the database
class User(db.Model, UserMixin):
    #__tablename__='users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), index=True, nullable=False)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    middle_name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    last_name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)#should be 128 in length to store hash
    dob = db.Column(db.String(255))
    pnumber = db.Column(db.Integer)
    address = db.Column(db.String(255))



    #THis is like a list with all the users notes and stuff
    notes = db.relationship('Note')