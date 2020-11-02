from flask import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import Form, TextField, PasswordField, BooleanField, validators
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mysqldb import MySQL
from MySQLdb import escape_string
from dbconnect import connection
from passlib.hash import sha256_crypt
import gc, re
import json
import requests
from functools import wraps

import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '999999999999999'
app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'csds393'
app.config['MYSQL_PASSWORD'] = 'moneyline'
app.config['MYSQL_DB'] = 'MoneyLine'

# Intialize MySQL
db = MySQL(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/antho/Documents/login-example/database.db'
# bootstrap = Bootstrap(app)
# db = SQLAlchemy(app)
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'
# db = SQLAlchemy(app)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'loggedin' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('index'))

    return wrap

@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash("You need to log in first")
    return redirect(url_for('index'))

@ app.route('/', methods=["GET", "POST"])
def index():
    error = ''
    c, conn = connection()
    try:
        if request.method == "POST":
            input_username = request.form['username']
            input_password = str(request.form['pswrd'])
            c.execute("SELECT * FROM users WHERE user_username = % s", (escape_string(input_username),))
            data = c.fetchone()
        
            if input_password == data[3]:
                session['loggedin'] = True
                session['username'] = input_username
                return redirect(url_for("threads"))
            else:
                error = "Invalid credential! Please try again."

        gc.collect()
        return render_template("login.html", error = error)
    except Exception as e:
        error = e
        return render_template("login.html")

@ app.route('/signup', methods=["GET", "POST"])
def signup():
    message = ''
    if request.method == "POST" and 'username' in request.form and 'pswrd' in request.form and 'email' in request.form:
        username = request.form['username']
        email = request.form['email']
        password = str(request.form['pswrd'])
        confirm_pw = str(request.form['cfpw'])
        c, conn = connection()

        c.execute("SELECT * FROM users WHERE user_username = % s", (escape_string(username),))
        acct = c.fetchone()
        
        if acct:
            message = 'Username already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username): 
            message = "Invalid username!"
        elif not username or not password or not email:
            message = "Missing information!"
        elif password != confirm_pw:
            message = 'Password not match, please try again'
        else:
            c.execute("INSERT INTO users (user_username, user_password, user_email) VALUES (%s, %s, %s)", (escape_string(username), escape_string(password), escape_string(email)))               
            conn.commit()
            message = "Thank you for registering. Welcome to MoneyLine!"
            return redirect(url_for("index"))

    elif request.method == 'POST':
        message = "Missing information! (Fill out)"        

    return render_template("signup.html", message=message)

@ app.route('/reset_pw')
def reset_pw():
    return render_template('reset_pw.html')

@ app.route('/threads')
@login_required
def threads():
    c, conn = connection()
    c.execute("SELECT * FROM posts ORDER BY post_posted DESC LIMIT 5")
    posts = c.fetchall()
    user1, user2, user3, user4, user5 = (post[1] for post in posts)
    body1, body2, body3, body4, body5 = (post[2] for post in posts)

    return render_template('threads.html', user1=user1, user2=user2, user3=user3, user4=user4, user5=user5, body1=body1, body2=body2, body3=body3, body4=body4, body5=body5)

@ app.route('/games')
@login_required
def games():
    f = open('odds.json')
    odds = json.load(f)

    for odd in odds:
        team1, team2 = odd['teams']
        odds = []
        for site in odd['sites']:
            odds.append(site['odds']['h2h'])
        print(team1,',', team2, odds)
        print()
    return render_template('games.html')

@ app.route('/faq')
@login_required
def faq(content=None):
    with open('static/betting101.txt', 'r') as f: 
        content = f.readlines()
        content = [x.strip() for x in content]
    return render_template('faq.html', content=content)

@ app.route('/profile')
@login_required
def profile():
    username = session['username']
    c, conn = connection()
    c.execute("SELECT * FROM users WHERE user_username = % s", (escape_string(username),))
    acct = c.fetchone()
    name = acct[1]
    if name is None:
        name = username
        c.execute("UPDATE users SET user_name = %s WHERE user_username = %s", (escape_string(name), escape_string(username)))
    return render_template('profile.html', name=name, username=username)
def avatar(self, size):
        digest = md5(username.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

@ app.route('/newPost', methods=["GET", "POST"])
@login_required
def add_post():
    message =''
    if request.method == "POST" and 'post' in request.form:
        username = session['username']
        post = request.form['post']
        c, conn = connection()

        c.execute("INSERT INTO posts (post_username, post_bodytext) VALUES (%s, %s)", (escape_string(username), escape_string(post)))       
        conn.commit()
        return redirect(url_for("threads"))

    elif request.method == 'POST':
        message = 'Please add body text!'

    return render_template('add_post.html',message=message)

@ app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)
