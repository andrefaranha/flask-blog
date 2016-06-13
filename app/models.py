from app import db
from werkzeug import generate_password_hash, check_password_hash


class User(db.Model):
    email = db.Column(db.String(120), primary_key=True)
    password = db.Column(db.String(120), unique=True)
    name = db.Column(db.String(64))

    def __init__(self, email, password, name):
        self.email = email
        self.password = generate_password_hash(password)
        self.name = name

    def __repr__(self):
        return '<User %r>' % (self.name)
