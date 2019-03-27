from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# For many to many relation ship with roles
# A single user can have many roles
# A single Role can have many users
user_roles_association = db.Table('user_role',
    db.Column('user_id',db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id',db.Integer, db.ForeignKey('role.id'), primary_key=True),
    db.Column('created_at',db.TIMESTAMP, server_default=db.func.now())
)

# Users model and related db columns
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    created_at = db.Column('created_at',db.TIMESTAMP, server_default=db.func.now())

    roles = db.relationship('Role', secondary=user_roles_association)

    # What gets printed in flask shell or yarn shell when
    # querying Users
    def __repr__(self):
        return '<User {}>'.format(self.username, self.email, self.created_at)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # For checking if a user has said role
    def has_role(self,role_sym):
        return [True if role.name == role_sym else False for role in self.roles]

# Roles model and related db columns
class Role(db.Model):
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
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(64), index=True, unique=True)
    text = db.Column(db.Text, index=True, unique=True)
    created_at = db.Column('created_at',db.TIMESTAMP, server_default=db.func.now())
    # A Topic can have many lessons
    lessons = db.relationship('Lesson', backref='lesson', lazy='dynamic')

    # What gets printed in flask shell or yarn shell when
    # querying topics
    def __repr__(self):
        return '<Topic {}>'.format(self.name, self.description, self.created_at)

# Lessons model and related db columns
class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(64), index=True, unique=True)
    text = db.Column(db.Text, index=True, unique=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))

    # What gets printed in flask shell or yarn shell when
    # querying Lessons
    def __repr__(self):
        return '<Topic {}>'.format(self.name, self.description, self.created_at)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
