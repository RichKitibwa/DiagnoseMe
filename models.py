from flask_login import UserMixin
from config import db
from config import create_app
from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy(create_app())


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    role = db.Column(db.String(1000))

    def __init__(self, email, password, name, role):
        db.create_all()
        self.email = email
        self.password = password
        self.name = name
        self.role = role

    def __repr__(self):
        return '<User %r>' % self.id
