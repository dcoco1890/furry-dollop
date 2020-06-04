import os

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp

# init app
app = Flask(__name__)

# Moved config to it's own file
app.config.from_pyfile('config.py')
# Session stuff
Session(app)

@app.route("/")
def index():
    return render_template("index.html")



