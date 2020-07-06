import os
import math
from flask import request, render_template, make_response, session, redirect, flash, jsonify
from datetime import datetime as dt
from flask import current_app as app
from .models import db, User
from werkzeug.security import check_password_hash, generate_password_hash

from .helpfunc import lookup_word


@app.route("/", methods=['GET'])
def home():

    return render_template("index.html")


@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect("/")


@app.route("/login", methods=['GET', 'POST'])
def login():
    # Forget any other user that may be logged in
    session.clear()

    if request.method == 'POST':
        # Just making sure we get valid input from the user
        if not request.form.get("username"):
            return make_response("No Username Provided", 404)
        elif not request.form.get("password"):
            return make_response("No password provided", 404)
        else:
            # Grab values from form + db
            u_name = request.form.get('username')
            u_pass = request.form.get('password')
            dbhash = User.query.filter_by(name=u_name).first()

            # If no user is found with that name flash msg and redirect to login
            if dbhash is None:
                flash("Login failed, please try again")
                return render_template("/login.html")
            # Do the same thing if the password hash does not match hash val in db
            if not check_password_hash(dbhash.hash, u_pass):
                flash("Login failed, please try again")
                return render_template("/login.html")
            # Save user id and name in session
            session['user_id'] = dbhash.id
            session['user_name'] = dbhash.name

            return redirect("/")
    else:
        # GET request on /login takes users to login form
        return render_template('login.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # The page itself has a required html tag, so this will probably not ever run
        if not request.form.get("username"):
            return make_response("No Username Provided", 404)
        elif not request.form.get("password"):
            return make_response("No password provided", 404)
        else:
            # Grab values from form + db
            u_name = request.form.get('username')
            u_pass = request.form.get('password')
            conf = request.form.get('confirmpass')
            user = User.query.filter(User.name == u_name).first()

            # Verify passwords match, and username is not already taken. Redirect/reload page if true
            if u_pass != conf:
                flash("Passwords do not match!")
                return redirect("/register")
            if user:
                flash("Username already taken!")
                return redirect("/register")

            # Create hash of user's password
            hashed_pass = generate_password_hash(u_pass)
            # Create new user and commit to db
            new_user = User(name=u_name, hash=hashed_pass, created=dt.now())
            db.session.add(new_user)
            db.session.commit()
            # Redirect user to login page
            return redirect("/login")
    else:
        return render_template("register.html")


@app.route("/lookup", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        word = request.form.get("word")
        defined_word = lookup_word(word)
        if not defined_word:
            flash("not working")
            return redirect("/lookup")
        else:
            return jsonify(defined_word)
    else:
        return render_template("lookup.html")
