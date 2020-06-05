from . import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    hash = db.Column(db.String(200))
    created = db.Column(db.DateTime)

    def __repr__(self):
        return '<User {}>'.format(self.name)

