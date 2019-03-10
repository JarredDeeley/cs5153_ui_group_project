from flask import render_template, flash, redirect, request, url_for, g
from flask_login import current_user, login_user, login_required, logout_user
from app import app, db, config
from app.models import User, Role
from app.forms import LoginForm, RegistrationForm
from flask_bouncer import requires
from flask_classy import FlaskView # To make managing app routes easier

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

# Simple solution not secure
@app.before_request
def load_user():
    g.user = current_user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(u'Invalid username or password','error')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        flash(u'Successfully Signed in!!!', 'success')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(u'Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash(u'Successfully Signed out', 'success')
    return redirect(url_for('index'))

# Admin interface class's
class AdminView(FlaskView):
    decorators = [login_required]

    # Index for admin dashboard
    def index(self):
        return render_template('admin/dashboard.html', title='Admin Dashboard')

class AdminRoleView(FlaskView):
    decorators = [login_required]

    # Route for all roles
    def index(self):
        roles = Role.query.all()
        return render_template('admin/roles/index.html', title='Roles', roles=roles)

    @app.route('/admin/role/<id>', methods=['GET'])
    @app.route('/admin/role/<id>/show', methods=['GET'])
    def show_role(self, id):
        role = Role.querry.get(id)
        return render_template('admin/roles/show.html', role=role)

    @app.route('/admin/role/<id>/edit', methods=['GET','POST'])
    def edit_role(self, id):
        role = Role.querry.get(id)
        return render_template('admin/roles/edit.html', role=role)

class AdminUserView(FlaskView):
    decorators = [login_required]

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

    @app.route('/admin/user/<id>', methods=['GET'])
    @app.route('/admin/user/<id>/show', methods=['GET'])
    def show_user(self, id):
        user = User.querry.get(id)
        return render_template('admin/users/show.html', user=user)

    @app.route('/admin/user/<id>/edit', methods=['GET','POST'])
    def edit_user(self, id):
        user = User.querry.get(id)
        return render_template('admin/users/edit.html', user=user)
