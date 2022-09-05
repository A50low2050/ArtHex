from app.database import db
from flask_login import UserMixin


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True, nullable=True)
    email = db.Column(db.String(50), unique=True, nullable=True)
    password = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f'<users {self.id}>'


class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.LargeBinary, unique=True, nullable=True, default=None)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'<profiles {self.id}>'


class Pictures(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=False, nullable=True)
    filename = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.Text, unique=False, nullable=False)

    def __repr__(self):
        return f'<pictures {self.id}>'
