from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

# Global stuff
db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_pyfile('../config.py')
    db.init_app(app)
    Session(app)

    with app.app_context():
        from . import routes
        db.create_all()

        return app

