from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func
from .default_themes import userThemeDefault, postThemeDefault


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150),unique=True)
    email = db.Column(db.String(150),unique=True)
    passwordHash =  db.Column(db.String(300))
    creationDate = db.Column(db.DateTime(timezone=True), default=func.now())
    userTheme = db.Column(db.Text, default=userThemeDefault)
    postTheme = db.Column(db.Text, default=postThemeDefault)
    posts = db.relationship('Post', backref='user', passive_deletes=True)
    weBring = db.Column(db.Boolean, default=False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    creationDate = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)