from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# For many to many relation ship with roles
user_roles_association = db.Table('user_role',
    db.Column('user_id',db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id',db.Integer, db.ForeignKey('role.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    roles = db.relationship('User', secondary=user_roles_association)
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(1500), index=True, unique=True)
    users = db.relationship('Role', secondary=user_roles_association)

    def __repr__(self):
        return '<Role {}>'.format(self.name)
