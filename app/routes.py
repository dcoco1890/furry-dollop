from flask import request, render_template, make_response, session
from datetime import datetime as dt
from flask import current_app as app
from .models import db, User


@app.route("/", methods=['GET'])
def home():
    return render_template("index.html")


@app.route("/add", methods=['GET'])
def create_user():
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
