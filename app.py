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
from MySQLdb import escape_string
from dbconnect import connection
from passlib.hash import sha256_crypt
import gc, re

import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '999999999999999'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/antho/Documents/login-example/database.db'
# bootstrap = Bootstrap(app)
# db = SQLAlchemy(app)
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'
db = SQLAlchemy(app)

@ app.route('/', methods=["GET", "POST"])
def index():
    error = ''
    c, conn = connection()
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

@ app.route('/signup', methods=["GET", "POST"])
def signup():
    message = ''
    if request.method == "POST" and 'username' in request.form and 'pswrd' in request.form and 'email' in request.form:
        username = request.form['username']
        email = request.form['email']
        password = str(request.form['pswrd'])
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
        else:
            c.execute("INSERT INTO users (user_username, user_password, user_email) VALUES (%s, %s, %s)", (escape_string(username), escape_string(password), escape_string(email)))               
            conn.commit()
            message = "Thank you for registering. Welcome to MoneyLine!"

    elif request.method == 'POST':
        message = "Missing information! (Fill out)"        

    return render_template("signup.html", message=message)

@ app.route('/reset_pw')
def reset_pw():
    return render_template('reset_pw.html')

@ app.route('/threads')
def threads():
    return render_template('threads.html')

@ app.route('/games')
def games():
    
    import json
    import requests


    api_key = '0c99967b1d1c94b6e0a2a1fa4e2379db'



    sports_response = requests.get('https://api.the-odds-api.com/v3/sports', params={
        'api_key': api_key
    })

    sports_json = json.loads(sports_response.text)

    if not sports_json['success']:
        print(
            'There was a problem with the sports request:',
            sports_json['msg']
        )

    else:
        print()
        print(
            'Successfully got {} sports'.format(len(sports_json['data'])),
            'Here\'s the first sport:'
        )
        print(sports_json['data'][0])



# To get odds for a sepcific sport, use the sport key from the last request
#   or set sport to "upcoming" to see live and upcoming across all sports
    sport_key = 'upcoming'

    odds_response = requests.get('https://api.the-odds-api.com/v3/odds', params={
        'api_key': api_key,
        'sport': sport_key,
        'region': 'uk', # uk | us | eu | au
        'mkt': 'h2h' # h2h | spreads | totals
    })

    odds_json = json.loads(odds_response.text)
    if not odds_json['success']:
        print(
            'There was a problem with the odds request:',
            odds_json['msg']
      )

    else:
    # odds_json['data'] contains a list of live and 
    #   upcoming events and odds for different bookmakers.
    # Events are ordered by start time (live events are first)
        print()
        print(
            'Successfully got {} events'.format(len(odds_json['data'])),
            'Here\'s the first event:'
        )
        print(odds_json['data'][0])

    # Check your usage
        print()
        print('Remaining requests', odds_response.headers['x-requests-remaining'])
        print('Used requests', odds_response.headers['x-requests-used'])

    return render_template('games.html')

@ app.route('/faq')
def faq(content=None):
    with open('static/betting101.txt', 'r') as f: 
        content = f.readlines()
        content = [x.strip() for x in content]
    return render_template('faq.html', content=content)

@ app.route('/settings')
def settings():
    return render_template('settings.html')

@ app.route('/about')
def about():
    return 'About'

if __name__ == "__main__":
    app.run(debug=True)
