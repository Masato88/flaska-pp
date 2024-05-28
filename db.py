from flask_sqlalchemy import SQLAlchemy
from flaskblog import app
from datetime import datetime
import pytz
from flask_login import UserMixin,LoginManager
import os

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///blog.db'
app.config['SECRET_KEY'] = os.urandom(24)
database=SQLAlchemy(app)
login_manager=LoginManager()
login_manager.init_app(app)

class Post(database.Model):
    id=database.Column(database.Integer,primary_key=True)
    title=database.Column(database.String(50),nullable=False)
    body=database.Column(database.String(300),nullable=False)
    created_at = database.Column(database.DateTime,nullable=False,default=datetime.now(pytz.timezone('Asia/Tokyo')))
    
class User(UserMixin,database.Model):
    id=database.Column(database.Integer,primary_key=True)
    username=database.Column(database.String(30),unique=True)
    password=database.Column(database.String(12))