from .app import db
from sqlalchemy_searchable import make_searchable
from sqlalchemy_utils.types import TSVectorType
from werkzeug import generate_password_hash, check_password_hash


make_searchable()


posts_tags_relationship_table = db.Table(
    'posts_tags_relationship_table',
    db.Column(
        'post_id', db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'),
        nullable=False,
    ),
    db.Column(
        'tag_id', db.Integer, db.ForeignKey('tag.id', ondelete='CASCADE'),
        nullable=False,
    ),
    db.PrimaryKeyConstraint('post_id', 'tag_id')
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(60), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author')

    def __init__(self, login, password, name):
        self.login = login
        self.set_password(password)
        self.name = name

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r: %r>' % (self.login, self.name)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    content = db.Column(db.Unicode, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags = db.relationship(
        'Tag', secondary=posts_tags_relationship_table, backref='posts'
    )
    search_vector = db.Column(TSVectorType('title', 'content'))

    def __init__(self, title, content, datetime, user_id):
        self.title = title
        self.content = content
        self.datetime = datetime
        self.user_id = user_id

    def __repr__(self):
        return '<Post "%r">' % (self.title)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Tag "%r">' % (self.name)
