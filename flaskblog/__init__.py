from flask import Flask
app = Flask(__name__) #多分絶対書くやつ
import flaskblog.main

import flaskblog.db
with app.app_context():
    db.database.create_all()
