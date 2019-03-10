from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_principal import Principal, Permission, RoleNeed

app = Flask(__name__,static_folder="../public",template_folder="./templates")
config = app.config.from_object(Config) # load config file
db = SQLAlchemy(app)   # SQLAlchemy database relations
migrate = Migrate(app, db) # for database migrations
login = LoginManager(app)
login.login_view = 'login'

principals = Principal(app)
admin_permission = Permission(RoleNeed('admin'))

# For recaptcha verification api keys
app.config['RECAPTCHA_USE_SSL']= False
app.config['RECAPTCHA_PUBLIC_KEY']='6LeGm5MUAAAAANEb9x2q5C1iwGp8mLgfy6xHRoB6'
app.config['RECAPTCHA_PRIVATE_KEY']='6LeGm5MUAAAAAC74Uo4F-LGf90AZfzDjiXDmFhJw'
app.config['RECAPTCHA_OPTIONS']= {'theme':'black'}

# Register add routes to make managing application easier
from app import routes, models
from faker import Faker
from werkzeug.security import generate_password_hash

# app routes registration
routes.AdminView.register(app,route_base='/admin')
routes.AdminUserView.register(app,route_base='/admin/users')
routes.AdminRoleView.register(app,route_base='/admin/roles')

# For Flask Shell
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': models.User, 'Role': models.Role}

# For database population/seeding
@app.cli.command()
def db_seed():
    faker = Faker()
    db.create_all()
    # Creating role
    if db.session.query(models.Role.id).filter_by(name='admin').scalar() is None:
        r = models.Role(name='admin',description='The all powerfull admin!!!')
        db.session.add(r)
        db.session.commit()

    # Create admin user
    if db.session.query(models.User.id).filter_by(username='admin').scalar() is None:
        u = models.User(username='admin',
                 email='admin@example.com',
                 password_hash=generate_password_hash('admin'))
        db.session.add(u)
        db.session.commit()
        u.roles.append(models.Role.query.get(1)) # add admin role
        db.session.commit()

    # Create random 100 users
    for _ in range(100):
        u = models.User(username=faker.name().lower().replace(" ", ""),
                 email=faker.email(),
                 password_hash=generate_password_hash('Password1234'))
        db.session.add(u)
        db.session.commit()

# Command line option to display current routes
@app.cli.command()
def list_routes():
    print(app.url_map)
