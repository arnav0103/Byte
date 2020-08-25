from Bytes import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

usertime = db.Table('usertime',
  db.Column('user_id', db.Integer , db.ForeignKey('users.id')),
  db.Column('time_id', db.Integer , db.ForeignKey('date.id')))

class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(64))
    username = db.Column(db.String , unique = True)
    profile_image = db.Column(db.String(64), nullable = False , default = 'head_res.png')
    email = db.Column(db.String(64),unique = True,index = True)
    password_hash = db.Column(db.String(128))

    timing = db.relationship('Time' , secondary = usertime , backref = db.backref('users', lazy = 'dynamic'))

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __init__(self, name,username, email, password ):
        self.email = email
        self.name =name
        self.username = username
        self.password_hash = generate_password_hash(password)

class Train(db.Model):
    __tablename__ = 'train'
    id = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String)

    date = db.relationship('Time' , backref = 'train' , lazy = 'dynamic')

    def __init__(self, name):
        self.name = name

class Time(db.Model):
    __tablename__ = 'date'
    id = db.Column(db.Integer , primary_key = True)

    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    start_place = db.Column(db.String)
    end_place = db.Column(db.String)
    seats = db.Column(db.Integer)

    trainid = db.Column(db.Integer , db.ForeignKey('train.id'))
    price = db.Column(db.Integer , nullable = True)


    def __init__(self , start , end , start_place ,end_place, train , seats , price):
        self.start = start
        self.end = end
        self.start_place = start_place
        self.end_place = end_place
        self.trainid = train
        self.seats = seats
        self.end_place = end_place
        self.price = price
