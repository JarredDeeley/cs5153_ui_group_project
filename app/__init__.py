from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__,static_folder="../public",template_folder="./templates")
config = app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

app.config['RECAPTCHA_USE_SSL']= False
app.config['RECAPTCHA_PUBLIC_KEY']='6LeGm5MUAAAAANEb9x2q5C1iwGp8mLgfy6xHRoB6'
app.config['RECAPTCHA_PRIVATE_KEY']='6LeGm5MUAAAAAC74Uo4F-LGf90AZfzDjiXDmFhJw'
app.config['RECAPTCHA_OPTIONS']= {'theme':'black'}

from app import routes, models

# For database seeding and flask shell
from app.models import Role, User
from faker import Faker
from werkzeug.security import generate_password_hash

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Role': Role}

@app.cli.command()
def db_seed():
    faker = Faker()
    db.create_all()
    # Creating role
    if db.session.query(Role.id).filter_by(name='admin').scalar() is not None:
        pass
    else:
        r = Role(name='admin',description='The all powerfull admin!!!')
        db.session.add(r)
        db.session.commit()

    # Create admin user
    if db.session.query(User.id).filter_by(username='admin').scalar() is not None:
        pass
    else:
        u = User(username='admin',
                 email='admin@example.com',
                 password_hash=generate_password_hash('admin'))
        db.session.add(u)
        db.session.commit()
        u.roles.append(Role.query.get(1)) # add admin role
        db.session.commit()

    # Create 100 users
    for _ in range(100):
        u = User(username=faker.name().lower().replace(" ", ""),
                 email=faker.email(),
                 password_hash=generate_password_hash(faker.name()))
        db.session.add(u)
        db.session.commit()
