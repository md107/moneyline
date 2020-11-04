from flask import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message
from flask_bootstrap import Bootstrap
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
from forms import EditProfileForm

import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '999999999999999'

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
    ids = [post[0] for post in posts]
    users = [post[1] for post in posts]
    bodies = [post[2] for post in posts]
    data = zip(ids,users,bodies)
    id1, id2, id3, id4, id5 = (post[0] for post in posts)
    user1, user2, user3, user4, user5 = (post[1] for post in posts)
    body1, body2, body3, body4, body5 = (post[2] for post in posts)

    return render_template('threads.html', ids=ids, users=users, bodies=bodies, data=data,
                                            id1=id1, id2=id2, id3=id3, id4=id4, id5=id5,
                                            user1=user1, user2=user2, user3=user3, user4=user4, user5=user5, 
                                            body1=body1, body2=body2, body3=body3, body4=body4, body5=body5)

@ app.route('/games', methods=["GET", "POST"])
@login_required
def games():
    f = open('odds.json')
    odds = json.load(f)
    teams = []
    bets = []
    c, conn = connection()
    for odd in odds:
        team1, team2 = odd['teams']
        teams.append([team1, team2])
        curr_bets = []
        for site in odd['sites']:
            curr_bets.append(site['odds']['h2h'])
        bets.append(curr_bets)
        c.execute("SELECT * FROM allbets WHERE team1 = %s AND team2 = %s AND odd = %s;", [escape_string(team1), escape_string(team2), escape_string(str(curr_bets))])
        b = c.fetchone()
        if b:
            pass
        else:
            c.execute("INSERT INTO allbets (team1, team2, odd) VALUES (%s, %s, %s);", (escape_string(team1), escape_string(team2), escape_string(str(curr_bets))))
            conn.commit()
    data = zip(teams, bets)

    if request.method == 'POST':
        username = session['username']

    return render_template('games.html', data=data)

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

@ app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

    
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

@app.route('/threads/<thread_id>', methods=["GET", "POST"])
@login_required
def page(thread_id):
    thread_id = thread_id
    c, conn = connection()
    c.execute("SELECT * FROM posts WHERE post_id = %s", thread_id)
    thread = c.fetchone()
        
    if request.method == "GET":
        c.execute("SELECT * FROM comments WHERE comment_thread_id = %s", thread_id)
        comments = c.fetchall()
        users = [c[2] for c in comments]
        dates = [c[4].strftime("%m/%d/%y %H:%M:%S") for c in comments]
        comments = [c[3] for c in comments]
        data = zip(users, comments, dates)
        print(dates)
        return render_template('thread_detail.html', id=thread[0], username=thread[1], bodytext=thread[2], date_posted=thread[3], data=data)
    elif request.method == "POST" and 'post' in request.form:
        username = session['username']
        post = request.form['post']
        if not post:
            return redirect(f"/threads/{thread_id}")
        c.execute("INSERT INTO comments (comment_thread_id, comment_username, comment_bodytext) VALUES (%s, %s, %s)", (thread_id, escape_string(username), escape_string(post)))
        conn.commit()
        return redirect(f"/threads/{thread_id}")
    elif request.method == 'POST':
        message = 'Missing information'
        return redirect(f"/threads/{thread_id}")

@app.route('/myList')
@login_required
def myList():
    username = session['username']
    c, conn = connection()
    c.execute("SELECT * FROM betlists WHERE username = %s;", (escape_string(username),))
    data = c.fetchall()
    bet_ids = [d[0] for d in data]
    bets = []
    for bet_id in bet_ids:
        c.execute("SELECT team1, team2, odd FROM allbets WHERE bet_id = %s;", (bet_id,))
        team1, team2, odd = c.fetchone()
        odd=odd.replace('[[', '').replace(']]', '')
        odd=odd.split('], [')
        bets.append([team1, team2, odd])
    return render_template('my_list.html', bets=bets)

@ app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)
