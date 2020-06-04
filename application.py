# import os
#
# from flask import Flask, flash, jsonify, redirect, render_template, request, session
# from flask_session import Session
# from flask_sqlalchemy import SQLAlchemy
#
# # init app and configuration
# app = Flask(__name__)
# app.config.from_pyfile('config.py')
#
# # Session stuff
# Session(app)
#
# db = SQLAlchemy(app)
#
#
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), unique=True)
#     hash = db.Column(db.String(200))
#
#     def __init__(self, name, hash):
#         self.name = name
#         self.hash = hash
#
#
# @app.route("/")
# def index():
#     return render_template("index.html")
#
#
#
