from flask import Blueprint, render_template
#from . import db
from database_connection.dbconn import DBConn, DBUser
from app import app as auth

#auth_blueprint = Blueprint('auth', __name__)

'''
Exists but maybe keep for now
'''
@auth.route('/login')
def login():
    return render_template('login.html')

'''
dynamically generated
'''
#@auth.route('/signup')
#def signup():
#    return render_template('signup.html')

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
#from .Models import User
#from . import db
...

''' Maybe necessary
@auth.route('/login', methods=['POST'])
def login_handler():
    if request.form.get("email"):
        return signup_post(request)
    else:
        return login_post(request)
'''

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = DBConn().select_user(name) # if this returns a user, then the email already exists in database

    # TODO login vs signup pages
    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('User already exists')
        return redirect(url_for('auth.login'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    hash_pass = generate_password_hash(password, method='sha256')
    new_user = DBUser(username=name, email=email)

    # add the new user to the database
    DBConn().insert_user(new_user, hash_pass)

    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # TODO implement this?
    #remember = True if request.form.get('remember') else False
    remember = False

    user = DBConn().select_user(username)

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user: #TODO password stuff or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('/'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('/'))
