from flask import render_template, flash, redirect, request, url_for, g, send_from_directory
from flask_login import current_user, login_user, login_required, logout_user
from flask_ckeditor import upload_fail, upload_success
from flask_classy import FlaskView # To make managing app routes easier
from functools import wraps
from app import app, config
from app.models import *
from app.forms import *

# If you would like to view all routes in route file type
# yarn routes or flask list-routes
# Still working on making the output look better

# For user authorizations
def requires_role(role):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not current_user.has_role(role):
                flash(u'You are not authorized to view that','danger')
                return render_template('index.html', title='Home')
            return f(*args, **kwargs)
        return wrapped
    return wrapper

# This is used via the vairable back_url
# This allows users to go back to the page
# They were on before
def redirect_back(default):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)

# Simple solution to flask-classy issue but not secure
# We aren't starting a company it doesn't matter
@app.before_request
def load_user():
    g.user = current_user

# Route for uploading to files to the uploads folder
# in project root uploads
@app.route('/uploads/<filename>')
def uploaded_files(filename):
    path = app.config['UPLOADED_PATH']
    return send_from_directory(path, filename)

# Route on pulic facing internet
# To upload files
@app.route('/upload', methods=['POST'])
def upload():
    import os
    f = request.files.get('upload')
    extension = f.filename.split('.')[1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='Image only!')
    f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
    url = url_for('uploaded_files', filename=f.filename)
    return upload_success(url=url)

######################################
######################################
##                                  ##
##        Where Routes start        ##
##                                  ##
######################################
######################################

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(u'Invalid username or password','danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        flash(u'Successfully Signed in!!!', 'success')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        form.save()
        flash(u'Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash(u'Successfully Signed out', 'success')
    return redirect(url_for('index'))

######################################
######################################
##                                  ##
##    Start of Admin users Routes   ##
##                                  ##
######################################
######################################

class AdminView(FlaskView):
    decorators = [login_required, requires_role('admin')]

    # Index for admin dashboard
    def index(self):
        return render_template('admin/dashboard.html', title='Admin Dashboard')

class AdminRoleView(FlaskView):
    decorators = [login_required, requires_role('admin')]

    # Route for all roles
    def index(self):
        return render_template('admin/roles/index.html', title='Roles',
                                roles=Role.query.all())

    def post(self, msg):
        form = RoleForm()
        if form.validate_on_submit():
            # if a new entry create else update
            form.save(True) if msg == 'created' else form.save(False)
            flash(u'You have successfully %s the %s role!!' % (msg, form.name.data), 'success')
            return render_template('admin/roles/index.html', title='Roles',
                                    roles=Role.query.all())
    def delete(self, id):
        role = Role.query.get(id)
        name = role.name
        app.db.session.delete(role)
        app.db.session.commit()
        flash(u'You have successfully deleted the %s role!!' % (name), 'success')
        return render_template('admin/roles/index.html', title='Roles',
                                roles=Role.query.all())

    def new(self):
        return render_template('admin/roles/new.html', form=RoleForm(), msg='created',
                                back_url=redirect_back('AdminRoleView:index'))

    def edit(self, id):
        # This allows for form data to be filled
        role = Role.query.get(id)
        form = RoleForm()
        form.name.data = role.name
        form.description.data = role.description
        return render_template('admin/roles/edit.html', form=form, msg='updated',
                                id=id, back_url=redirect_back('AdminRoleView:index'))

    def show(self, id):
        return render_template('admin/roles/show.html', role=Role.query.get(id),
                                back_url=redirect_back('AdminRoleView:index'))

class AdminTopicView(FlaskView):
    decorators = [login_required, requires_role('admin')]

    # Route for all topics
    def index(self):
        return render_template('admin/topics/index.html', title='Topics',
                                topics=Topic.query.all())

    def post(self, msg):
        form = TopicForm()
        if form.validate_on_submit():
            # if a new entry create else update
            form.save(True) if msg == 'created' else form.save(False)
            flash(u'You have successfully %s the %s topic!!' % (msg, form.name.data), 'success')
            return render_template('admin/topics/index.html', title='Topics',
                                    topics=Topic.query.all())

    def new(self):
        return render_template('admin/topics/new.html', form=TopicForm(), msg='created',
                                back_url=redirect_back('AdminTopicView:index'))

    def edit(self, id):
        # This allows for form data to be filled
        topic = Topic.query.get(id)
        form = TopicForm()
        form.name.data = topic.name
        form.description.data = topic.description
        form.text.data = topic.text
        return render_template('admin/topics/edit.html', form=form, msg='updated',
                                id=id, back_url=redirect_back('AdminTopicView:index'))

    def show(self, id):
        return render_template('admin/topics/show.html', topic=Topic.query.get(id),
                                back_url=redirect_back('AdminTopicView:index'))

# Inheriting from AdminTopicView is just for naming conventions
# This allows for nested resources in flask
class AdminLessonView(AdminTopicView):
    decorators = [login_required, requires_role('admin')]

    def post(self, msg, tid):
        form = LessonForm()
        if form.validate_on_submit():
            # if a new entry create else update
            form.save(True) if msg == 'created' else form.save(False)
            flash(u'You have successfully %s the %s Lesson!!' % (msg, form.name.data), 'success')
            return render_template('admin/topics/lessons/show.html', lesson=Lesson.query.get(form.iden.data),
                                    tid=tid, back_url=redirect_back('AdminTopicView:index'))

    def new(self, tid):
        return render_template('admin/topics/lessons/new.html', form=LessonForm(), msg='created',
                                tid=tid, back_url=redirect_back('AdminTopicView:index'))

    def edit(self, id, tid):
        # This allows for form data to be filled
        lesson = Lesson.query.get(id)
        form = LessonForm()
        form.name.data = lesson.name
        form.description.data = lesson.description
        form.text.data = lesson.text
        return render_template('admin/topics/lessons/edit.html', form=form, msg='updated', id=id,
                                tid=tid, back_url=redirect_back('AdminTopicView:index'))

    def show(self, id, tid):
        return render_template('admin/topics/lessons/show.html', lesson=Lesson.query.get(id),
                                tid=tid, back_url=redirect_back('AdminTopicView:index'))

class AdminUserView(FlaskView):
    decorators = [login_required, requires_role('admin')]

    # Route for all users
    def index(self):
        page = request.args.get('page', 1, type=int)
        users = User.query.paginate(page, 10, False)
        next_url = url_for('AdminUserView:index', page=users.next_num) \
            if users.has_next else None
        prev_url = url_for('AdminUserView:index', page=users.prev_num) \
            if users.has_prev else None
        return render_template('admin/users/index.html', title='Users',
                                users=users.items, next_url=next_url,
                                prev_url=prev_url)

    def post(self):
        form = UserForm()
        if form.validate_on_submit():
            form.save()
            flash(u'You have successfully udated user %s' % (form.username.data), 'success')
            return render_template('admin/users/index.html', title='Users',
                                    users=User.query.all())

    def edit(self, id):
        # This allows for form data to be filled
        user = User.query.get(id)
        form = UserForm()
        form.username.data = user.username
        form.email.data = user.email
        return render_template('admin/users/edit.html', form=form, id=id,
                                 back_url=redirect_back('AdminUserView:index'))

    def show(self, id):
        return render_template('admin/users/show.html', user=User.query.get(id),
                                back_url=redirect_back('AdminUserView:index'))

######################################
######################################
##                                  ##
## Start of Non Admin users Routes  ##
##                                  ##
######################################
######################################

class TopicView(FlaskView):
    # Route for all topics
    def index(self):
        return render_template('topics/index.html', title='Topics',
                                topics=Topic.query.all())

    def show(self, id):
        return render_template('topics/show.html', topic=Topic.query.get(id),
                                back_url=redirect_back('TopicView:index'))

# Inheriting from TopicView is just for naming conventions
# This allows for nested resources in flask
class LessonView(TopicView):

    def show(self, id, tid):
        return render_template('topics/lessons/show.html', lesson=Lesson.query.get(id),
                                tid=tid, back_url=redirect_back('TopicView:index'))
