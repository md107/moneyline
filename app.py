from flask import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message

app = Flask(__name__)
# app.config['...']

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

@ app.route('/')
def index():
    return render_template('login.html')

@ app.route('/signup')
def signup():
    return render_template('signup.html')

@ app.route('/reset_pw')
def reset_pw():
    return render_template('reset_pw.html')

@ app.route('/threads')
def threads():
    return render_template('threads.html')

@ app.route('/games')
def games():
    return render_template('games.html')

@ app.route('/faq')
def faq():
    return render_template('faq.html')

@ app.route('/settings')
def settings():
    return render_template('settings.html')

@ app.route('/about')
def about():
    return 'About'

if __name__ == "__main__":
    app.run(debug=True)