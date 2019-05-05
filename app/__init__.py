### Not the best web application, but she gets the job done ###

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_wtf import CSRFProtect
from logging import basicConfig, DEBUG

app = Flask(__name__,static_folder="../public",template_folder="./templates")
config = app.config.from_object(Config) # load config file
db = SQLAlchemy(app)   # SQLAlchemy database relations
migrate = Migrate(app, db) # for database migrations
ckeditor = CKEditor(app) # For content management system (CMS)
login = LoginManager(app) # For user login
csrf = CSRFProtect(app)
login.login_view = 'login'

basicConfig(filename="user_log.txt",
            filemode='a',
            level=DEBUG)

# Register add routes to make managing application easier
from app import routes, models, topic_lesson_content_seed
from faker import Faker
from werkzeug.security import generate_password_hash

# Just encase some anonymous user wants to do something
login.anonymous_user = models.Anonymous

# Admin users routes registration
routes.AdminView.register(app,route_base='/admin')
routes.AdminUserView.register(app,route_base='/admin/users')
routes.AdminRoleView.register(app,route_base='/admin/roles')
routes.AdminTopicView.register(app,route_base='/admin/topics')
routes.AdminLessonView.register(app,route_base='/admin/topics/<tid>/lessons')

# Regular users routes registration
routes.TopicView.register(app,route_base='/topics')
routes.LessonView.register(app,route_base='/topics/<tid>/lessons')
routes.CommentView.register(app,route_base='/topics/<tid>/lessons/<lid>/comments')
routes.UserView.register(app,route_base='/account')
routes.BookmarkView.register(app,route_base='/bookmarks')

# For Flask Shell
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': models.User, 'Role': models.Role,
            'Topic': models.Topic, 'Lesson': models.Lesson,
            'Comment': models.Comment, 'Bookmark': models.Bookmark }

# For database population/seeding
@app.cli.command()
def db_seed():
    faker = Faker()
    db.create_all()

    # Create topic and lesson content
    topic_lesson_content_seed.seed_topic_and_lesson_content(db)

    # Create admin role
    if db.session.query(models.Role.id).filter_by(name='admin').scalar() is None:
        r = models.Role(name='admin',description='The all powerfull admin!!!')
        db.session.add(r)
        db.session.commit()

    # Create admin user
    if db.session.query(models.User.id).filter_by(username='admin').scalar() is None:
        u = models.Use(username='admin',
                 email='admin@example.com',
                 password_hash=generate_password_hash('admin'),
 	         name='admin',
		 contact=123)
        db.session.add(u)
        db.session.commit()
        u.roles.append(models.Role.query.get(1)) # add admin role
        db.session.commit()

    # Create random 5 users
    for _ in range(5):
        u = models.User(username=faker.name().lower().replace(" ", ""),
                 email=faker.email(),
                 password_hash=generate_password_hash('Password1234'),
		 name=faker.name(),
		 contact=0)
        db.session.add(u)
        db.session.commit()

# Command line option to display current routes
@app.cli.command()
def list_routes():
    print(app.url_map)
