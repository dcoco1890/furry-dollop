from flask import request, render_template, make_response, session, redirect, flash, url_for
from datetime import datetime as dt
from flask import current_app as app
from .models import db, User
from werkzeug.security import check_password_hash, generate_password_hash

from .helpfunc import login_required


@app.route("/", methods=['GET'])
def home():
    return render_template("index.html")


@app.route("/add", methods=['GET'])
def create_user():
    # Most of this stuff is just testing to make sure things work, will remove
    # TODO make this better
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
            if dbhash is None or not check_password_hash(dbhash.hash, u_pass):
                flash("Login failed, please try again")
                return redirect("/login")
            # Do the same thing if the password hash does not match hash val in db
            # if not check_password_hash(dbhash.hash, u_pass):
            #     flash("Login failed, please try again")
            #     return redirect("/login")

            session['user_id'] = dbhash.id
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


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        return redirect(url_for("upload"))
    else:
        return render_template("upload.html")
