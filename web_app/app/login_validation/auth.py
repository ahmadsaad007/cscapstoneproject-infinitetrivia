from flask import Blueprint, render_template, session
#from . import db
from database_connection.dbconn import DBConn, DBUser
from app import app as auth

#auth_blueprint = Blueprint('auth', __name__)

'''
Exists but maybe keep for now
'''
#@auth.route('/login')
#def login():
#    return render_template('login.html')

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

#Maybe necessary
#@auth.route('/login', methods=['POST'])
def login_handler():
    if request.form.get("email"):
        return signup_post(request)
    else:
        return login_post(request)


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    print("Signup for: ", request.form.get("email"), request.form.get('username'), request.form.get('password'))

    user = DBConn().select_user(username) # if this returns a user, then the email already exists in database

    # TODO login vs signup pages
    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('User already exists')
        return redirect(url_for('login_page'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    hash_pass = generate_password_hash(password)
    new_user = DBUser(username=username, email=email)

    # add the new user to the database
    DBConn().insert_user(new_user, hash_pass)

    return redirect(url_for('login_page'))

@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    
    print(username, password)
    # TODO implement this?
    #remember = True if request.form.get('remember') else False
    remember = False

    user = DBConn().select_user(username)
    if user is None:
        print("User not found")

    if user is not None and check_password_hash(DBConn().select_password(user.username), password):
        print("Logging user", username, "in")
        session.permanent = True
        session['username'] = user.username
        return redirect(url_for('index'))
    
    print("Password A:", DBConn().select_password(user.username))
    #print("Password B:", hash_pass)
    flash('Please check your login details and try again.')
    return redirect(url_for('login_page'))
    
    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    #if not user: #TODO password stuff or not check_password_hash(user.password, password):
    #    flash('Please check your login details and try again.')
    #    return redirect(url_for('login_page')) # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    #session["username"] = username
    #return redirect(url_for('index'))

@auth.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    return redirect(url_for('/'))
