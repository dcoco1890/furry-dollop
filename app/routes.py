from flask import request, render_template, make_response, session
from datetime import datetime as dt
from flask import current_app as app
from .models import db, User
from werkzeug.security import check_password_hash, generate_password_hash


@app.route("/", methods=['GET'])
def home():
    return render_template("index.html")


@app.route("/add", methods=['GET'])
def create_user():
    # Most of this stuff is just testing to make sure things work, will remove
    #TODO make this better
    un = request.args.get('user')
    p = request.args.get('pass')
    session['test'] = 'yes'
    x = session['test']
    print(x)
    if un and p:
        new_user = User(name=un, hash=p, created=dt.now())
        db.session.add(new_user)
        db.session.commit()
    users = User.query.all()
    return render_template("index.html", users=users)


@app.route("/login", methods=['GET', 'POST'])
def login():

    # commenting out for now as session is not really set up yet
    # session.clear

    if request.method == 'POST':
        # TODO verify user has entered information in the login form, validate
        # user exists in the db, checkpasshash, redirect to homepage
        return
    else:
        # GET request on /login takes users to login form
        return render_template('login.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    # TODO change validation stuff to use flashed messages to prevent hitting the back button
    if request.method == "POST":
        # The page itself has a required tag, so this will probably not ever run
        if not request.form.get("username"):
            return make_response("No Username Provided", 404)
        elif not request.form.get("password"):
            return make_response("No password provided", 404)
        else:
            # Grab values from form
            u_name = request.form.get('username')
            u_pass = request.form.get('password')
            conf = request.form.get('confirmpass')
            # If passwords don't match return this
            if u_pass != conf:
                return "Passwords must match"

            # Check is a user already exists
            user = User.query.filter(User.name == u_name).first()
            if user:
                return make_response(f"{user} already exists", 404)
            # Create hash of user's password
            hashed_pass = generate_password_hash(u_pass)
            # Create new user and commit to db
            new_user = User(name=u_name, hash=hashed_pass, created=dt.now())
            db.session.add(new_user)
            db.session.commit()
            # TODO change this to redirect to login. This was just to test and it worked
            users = User.query.all()
            return render_template("index.html", users=users)
    else:
        return render_template("register.html")
