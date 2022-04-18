from flask_login import UserMixin
from config import db
from sqlalchemy.sql import func
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
    files = db.relationship('Files', backref='user', lazy=True)

    def __init__(self, email, password, name, role):
        db.create_all()
        self.email = email
        self.password = password
        self.name = name
        self.role = role

    def __repr__(self):
        return '<User %r>' % self.id


class Files(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String(100))
    data = db.Column(db.LargeBinary)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, file, data, user_id):
        self.file = file
        self.data = data
        self.user_id = user_id
        db.create_all()

    def __repr__(self):
        return '<Files %r>' % self.id
