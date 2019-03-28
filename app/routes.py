from flask import render_template, flash, redirect, request, url_for, g, send_from_directory
from flask_login import current_user, login_user, login_required, logout_user
from flask_ckeditor import upload_fail, upload_success
from flask_classy import FlaskView # To make managing app routes easier
from functools import wraps
from app import app, config
from app.models import *
from app.forms import *

# For user authorizations
def requires_role(role):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not current_user.has_role(role):
                flash(u'You are not authorized to view that','error')
                return render_template('index.html', title='Home')
            return f(*args, **kwargs)
        return wrapped
    return wrapper

# Simple solution to flask-classy issue but not secure
# We aren't starting a company it doesn't matter
@app.before_request
def load_user():
    g.user = current_user

@app.route('/uploads/<filename>')
def uploaded_files(filename):
    path = app.config['UPLOADED_PATH']
    return send_from_directory(path, filename)

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

# Where actual routes start
@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(u'Invalid username or password','error')
            return redirect(url_for('index'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        flash(u'Successfully Signed in!!!', 'success')
        return redirect(next_page)
    return render_template('index.html', title='Home', form=form)
    #return render_template('index.html', title='Home')

#@app.route('/login', methods=['GET', 'POST'])
#def login():
#    if current_user.is_authenticated:
#        return redirect(url_for('index'))
#    form = LoginForm()
#    if form.validate_on_submit():
#        user = User.query.filter_by(username=form.username.data).first()
#        if user is None or not user.check_password(form.password.data):
#            flash(u'Invalid username or password','error')
#            return redirect(url_for('login'))
#        login_user(user, remember=form.remember_me.data)
#        next_page = request.args.get('next')
#        if not next_page or url_parse(next_page).netloc != '':
#            next_page = url_for('index')
#        flash(u'Successfully Signed in!!!', 'success')
#        return redirect(next_page)
#    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        form.save()
        flash(u'Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash(u'Successfully Signed out', 'success')
    return redirect(url_for('index'))

# Admin interface class's
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
            msg = msg.split(",")
            # if a new entry create else update
            form.save(msg[1],True) if msg[0] == 'created' else form.save(msg[1],False)
            flash(u'You have successfully %s the %s role!!' % (msg[0], form.name.data), 'success')
            return render_template('admin/roles/index.html', title='Roles',
                                roles=Role.query.all())

    def new(self):
        return render_template('admin/roles/new.html', form=RoleForm())

    def edit(self, id):
        return render_template('admin/roles/edit.html', form=RoleForm(),
                                role=Role.query.get(id), msg="updated,"+str(id))

    def show(self, id):
        return render_template('admin/roles/show.html', role=Role.query.get(id))

class AdminTopicView(FlaskView):
    decorators = [login_required, requires_role('admin')]

    # Route for all roles
    def index(self):
        return render_template('admin/topics/index.html', title='Topics',
                                topics=Topic.query.all())


    def post(self, msg):
        form = TopicForm()
        if form.validate_on_submit():
            msg = msg.split(",")
            # if a new entry create else update
            form.save(msg[0],True) if msg[0] == 'created' else form.save(msg[1],False)
            flash(u'You have successfully %s the %s topic!!' % (msg[0], form.name.data), 'success')
            return render_template('admin/topics/index.html', title='Topics',
                                topics=Topic.query.all())

    def new(self):
        return render_template('admin/topics/new.html', form=TopicForm())

    def edit(self, id):
        return render_template('admin/topics/edit.html', form=TopicForm(),
                                topic=Topic.query.get(id), msg="updated,"+str(id))

    def show(self, id):
        return render_template('admin/topics/show.html', topic=Topic.query.get(id))

class AdminUserView(FlaskView):
    decorators = [login_required, requires_role('admin')]

    # Route for users all
    def index(self):
        page = request.args.get('page', 1, type=int)
        users = User.query.paginate(page, 10, False)
        next_url = url_for('AdminUserView:index', page=users.next_num) \
            if users.has_next else None
        prev_url = url_for('AdminUserView:index', page=users.prev_num) \
            if users.has_prev else None
        return render_template('admin/users/index.html', title='Users', users=users.items,
                                next_url=next_url, prev_url=prev_url)

    def post(self, id):
        form = UserForm()
        if form.validate_on_submit():
            form.save(id)
            flash(u'You have successfully udated user %s' % (form.username.data), 'success')
            return render_template('admin/users/index.html', title='Users',
                                users=User.query.all())

    def edit(self, id):
        return render_template('admin/users/edit.html', form=UserForm(), user=User.query.get(id))

    def show(self, id):
        return render_template('admin/users/show.html', user=User.query.get(id))


