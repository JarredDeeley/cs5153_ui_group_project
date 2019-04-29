from app import app, db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
import flask_whooshalchemy as wa

# For many to many relationship with users,roles
# A single user can have many roles
# A single Role can have many users
user_roles_association = db.Table('user_role',
    db.Column('user_id',db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id',db.Integer, db.ForeignKey('role.id'), primary_key=True),
    db.Column('created_at',db.TIMESTAMP, server_default=db.func.now())
)

# For many to many relationship with comments,replies
# A single comment can have many replies
# A single reply can have many comments
comment_replies_association = db.Table('comment_reply',
    db.Column('comment_id',db.Integer, db.ForeignKey('comment.id'), primary_key=True),
    db.Column('reply_id',db.Integer, db.ForeignKey('reply.id'), primary_key=True),
    db.Column('created_at',db.TIMESTAMP, server_default=db.func.now())
)

class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.username = 'Guest'

    def has_role(self, role_sym):
        return False

# Users model and related db columns
class User(UserMixin, db.Model):
    __searchable__ = ['username','email']

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    created_at = db.Column('created_at',db.TIMESTAMP, server_default=db.func.now())

    roles = db.relationship('Role', secondary=user_roles_association)
    comments = db.relationship('Comment', backref='user', lazy='dynamic')
    bookmark = db.relationship('Bookmark', uselist=False, backref='user')

    # What gets printed in flask shell or yarn shell when
    # querying Users
    def __repr__(self):
        return '<User {}>'.format(self.username, self.email, self.created_at)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # For checking if a user has said role
    def has_role(self, role_sym):
        return [True if role.name == role_sym else False for role in self.roles]

# Roles model and related db columns
class Role(db.Model):
    __searchable__ = ['name','description']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(1500), index=True, unique=True)
    created_at = db.Column('created_at',db.TIMESTAMP, server_default=db.func.now())

    users = db.relationship('User', secondary=user_roles_association)

    # What gets printed in flask shell or yarn shell when
    # querying Roles
    def __repr__(self):
        return '<Role {}>'.format(self.name, self.description, self.created_at)

# Topics model and related db columns
class Topic(db.Model):
    __searchable__ = ['name','description']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(64), index=True, unique=True)
    text = db.Column(db.Text, index=True, unique=True)
    created_at = db.Column('created_at',db.TIMESTAMP, server_default=db.func.now())

    # A Topic can have many lessons
    lessons = db.relationship('Lesson', backref='lesson', lazy='dynamic')
    lesson = db.relationship('Lesson', uselist=False, backref='topic')

    bookmark = db.relationship('Bookmark', uselist=False, backref='topic')

    # What gets printed in flask shell or yarn shell when
    # querying topics
    def __repr__(self):
        return '<Topic {}>'.format(self.name, self.description, self.created_at)

# Lessons model and related db columns
class Lesson(db.Model):
    __searchable__ = ['name','description']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(64), index=True, unique=True)
    text = db.Column(db.Text, index=True, unique=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))
    created_at = db.Column('created_at',db.TIMESTAMP, server_default=db.func.now())

    # A single lesson can have many comments
    comments = db.relationship('Comment', lazy='dynamic')

    bookmark = db.relationship('Bookmark', uselist=False, backref='lesson')

    # What gets printed in flask shell or yarn shell when
    # querying Lessons
    def __repr__(self):
        return '<Lesson {}>'.format(self.name, self.description, self.created_at)

    def is_null(self):
        return self is None

    def is_int(self):
        return type(self.id) == 'int'

# Comment model and related db columns
class Comment(db.Model):
    __searchable__ = ['text']

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'))
    text = db.Column(db.Text, index=True, unique=True)
    created_at = db.Column('created_at',db.TIMESTAMP, server_default=db.func.now())

    replies = db.relationship('Reply', secondary=comment_replies_association)

    # What gets printed in flask shell or yarn shell when
    # querying Lessons
    def __repr__(self):
        return '<Comment {}>'.format(self.id, self.lesson_id, self.created_at)

# Reply model and related db columns
class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, index=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column('created_at',db.TIMESTAMP, server_default=db.func.now())

    comments = db.relationship('Comment', secondary=comment_replies_association)

    # What gets printed in flask shell or yarn shell when
    # querying Lessons
    def __repr__(self):
        return '<Reply {}>'.format(self.id, self.created_at)


# Bookmark model and related db columns
class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'))
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))

    created_at = db.Column('created_at',db.TIMESTAMP, server_default=db.func.now())

    # What gets printed in flask shell or yarn shell when
    # querying Lessons
    def __repr__(self):
        return '<Bookmark {}>'.format(self.id, self.lesson_id, self.user_id, self.topic_id, self.created_at)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

wa.whoosh_index(app, User)
wa.whoosh_index(app, Role)
wa.whoosh_index(app, Topic)
wa.whoosh_index(app, Lesson)
wa.whoosh_index(app, Comment)

