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
