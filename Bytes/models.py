from Bytes import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
    
class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(64))
    username = db.Column(db.String , unique = True)
    profile_image = db.Column(db.String(64), nullable = False , default = 'head_res.png')
    email = db.Column(db.String(64),unique = True,index = True)
    password_hash = db.Column(db.String(128))

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __init__(self, name,username, email, password ):
        self.email = email
        self.name =name
        self.username = username
        self.password_hash = generate_password_hash(password)
