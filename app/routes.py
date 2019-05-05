from flask import render_template, flash, redirect, request, url_for, g, send_from_directory
from urllib.parse import urlparse, urljoin
from flask_login import current_user, login_user, login_required, logout_user
from flask_ckeditor import upload_fail, upload_success
from flask_classy import FlaskView # To make managing app routes easier
from functools import wraps
from werkzeug.urls import url_parse
from app import app, config, db, login
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

# if user not logged in
@login.unauthorized_handler
def unauthorized():
    flash(u'You must sign in before usage!!','warning')
    app.logger.info('User warned that they need to login first')
    # redirect to login page if user not logged in
    return render_template('index.html', title='Home', form=LoginForm())

# http://flask.pocoo.org/snippets/62/
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

def get_redirect_target():
    for target in request.values.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target

# This is used via the vairable back_url
# This allows users to go back to the page
# They were on before
def redirect_back(endpoint, **values):
    target = request.referrer
    if not target or not is_safe_url(target):
       target = url_for(endpoint, **values)
    return redirect(target)

# Simple solution to flask-classy issue but not secure
# We aren't starting a company it doesn't matter
@app.before_request
def load_user():
    g.user = current_user
    if g.user.is_authenticated:
        g.search_form = SearchForm()

@app.route('/searching', methods=['POST'])
@login_required
def searching():
    app.logger.info('User performed a search')

    req = request.referrer[22:]
    req_topics = request.referrer[22:29]
    results = []
    if req ==  'faq' or req ==  'account/settings/':
        flash(u'The search option is only available for Topics and Lessons...', 'danger')
        return redirect_back('index')

    if not g.search_form.validate_on_submit():
        return redirect(url_for('index'))
    qr=g.search_form.search.data
    if req == 'topics/':
    	results = Topic.query.whoosh_search(qr).all()
    	return render_template('search_results.html', results=results,query=qr, page='Topics',
                                back_url=redirect_back('index'),bform=BookmarkForm())

    results = Lesson.query.whoosh_search(qr).all()
    return render_template('search_results.html', results=results,query=qr, page='Lessons',
                            back_url=redirect_back('index'))

    return redirect(url_for('index'))

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
@app.route('/index', methods=['GET', 'POST'])
def index():
    app.logger.info('User on home page')

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            app.logger.info('User failed to login')
            flash(u'Invalid username or password','danger')
            return redirect(url_for('index'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        flash(u'Successfully Signed in!!!', 'success')
        app.logger.info('User logged in successfully')

        return redirect(next_page)
    return render_template('index.html', title='Home', form=form)

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    app.logger.info('User on Registration page')

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        form.save()
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user)
        flash(u'Congratulations, you are now a registered user!', 'success')
        app.logger.info('User created new account')
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)
    return render_template('register.html', title='Register', form=form)

# Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()

    flash(u'Successfully Signed out', 'success')
    app.logger.info('User has been signed out')

    return render_template('index.html', title='Home', form=LoginForm())

# This route is need to redirect users to login
@app.route('/login', methods=['GET','POST'])
def login():
    app.logger.login('User on login page')

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(u'Invalid username or password','danger')
            app.logger.login('User failed login')

            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        flash(u'Successfully Signed in!!!', 'success')
        app.logger.info('User signed in')
        return redirect(next_page)
    return render_template('index.html', title='Home', form=form)

#FAQs
@app.route('/faq')
def faq():
    app.logger.info('User on FAQ page')
    return render_template('faq.html', title='FAQs', form=LoginForm())


######################################
######################################
##                                  ##
##    Start of Admin users Routes   ##
##                                  ##
######################################
######################################

class AdminView(FlaskView):
    decorators = [requires_role('admin'), login_required]

    # Index for admin dashboard
    def index(self):
        app.logger.info('On ADMIN dashboard')
        return render_template('admin/dashboard.html', title='Admin Dashboard')

class AdminRoleView(FlaskView):
    decorators = [requires_role('admin'), login_required]

    # Route for all roles
    def index(self):
        app.logger.info('On ADMIN role view')
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
    decorators = [requires_role('admin'), login_required]

    # Route for all topics
    def index(self):
        app.logger.info('on ADMIN topic view')
        return render_template('admin/topics/index.html', title='Topics',
                                topics=Topic.query.all())

    def post(self, msg):
        # have to cheese this to make work
        if (msg.isdigit()): # this if for delete
            topic = Topic.query.get(msg)
            name = topic.name
            topic.lessons.delete()
            db.session.delete(topic)
            db.session.commit()
            flash(u'You have successfully deleted the %s topic!!' % (name), 'success')
            return render_template('admin/topics/index.html', title='Topics',
                                    topics=Topic.query.all())
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
    decorators = [requires_role('admin'), login_required]

    def post(self, msg, tid):
        # have to cheese this to make work
        if (msg.isdigit()): # this if for delete
            lesson = Lesson.query.get(msg)
            name = lesson.name
            db.session.delete(lesson)
            db.session.commit()
            flash(u'You have successfully deleted the %s lesson!!' % (name), 'success')
            return render_template('admin/topics/show.html', topic=Topic.query.get(tid),
                                    back_url=redirect_back('AdminTopicView:index'))
        form = LessonForm()
        if form.validate_on_submit():
            # if a new entry create else update
            form.save(True) if msg == 'created' else form.save(False)
            flash(u'You have successfully %s the %s Lesson!!' % (msg, form.name.data), 'success')
            return render_template('admin/topics/lessons/show.html', lesson=Lesson.query.get(form.iden.data),
                                    back_url=redirect_back('AdminTopicView:index'))

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
                                back_url=redirect_back('AdminTopicView:index'))

class AdminUserView(FlaskView):
    decorators = [requires_role('admin'), login_required]

    # Route for all users
    def index(self):
        # I did this like this becuase I didn't want flask-classy to define another route
        page = request.args.get('page', 1, type=int)
        users = User.query.paginate(page, 10, False)
        next_url = url_for('AdminUserView:index', page=users.next_num) \
            if users.has_next else None
        prev_url = url_for('AdminUserView:index', page=users.prev_num) \
            if users.has_prev else None
        return render_template('admin/users/index.html', title='Users', users=users.items,
                                next_url=next_url, prev_url=prev_url,
                                back_url=redirect_back('AdminUserView:index'))

    def post(self):
        form = UserForm()
        if form.validate_on_submit():
            form.save()
            flash(u'You have successfully udated user %s' % (form.username.data), 'success')
            # I did this like this becuase I didn't want flask-classy to define another route
            page = request.args.get('page', 1, type=int)
            users = User.query.paginate(page, 10, False)
            next_url = url_for('AdminUserView:index', page=users.next_num) \
                if users.has_next else None
            prev_url = url_for('AdminUserView:index', page=users.prev_num) \
                if users.has_prev else None
            return render_template('admin/users/index.html', title='Users', users=users.items,
                                    next_url=next_url, prev_url=prev_url,
                                    back_url=redirect_back('AdminUserView:index'))
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
        app.logger.info('User on Topic page')
        return render_template('non_admin/topics/index.html', title='Topics',
                                topics=Topic.query.all(), bform=BookmarkForm())

    def show(self, id):
        app.logger.info('User viewing topic: {}'.format(Topic.query.get(id)))
        return render_template('non_admin/topics/show.html', topic=Topic.query.get(id),
                                bform=BookmarkForm(), back_url=redirect_back('TopicView:index'), form=form)

# Inheriting from TopicView is just for naming conventions
# This allows for nested resources in flask
class LessonView(TopicView):

    def show(self, id, tid):
        app.logger.info('User on Lesson page: {}'.format(Lesson.query.get(id)))
        return render_template('non_admin/topics/lessons/show.html', lesson=Lesson.query.get(id),
                                tid=tid, lid=id, form=CommentForm(), bform=BookmarkForm(), msg='created',
                                back_url=redirect_back('TopicView:index'))

# Inheriting from Lesson is just for naming conventions
# This allows for nested resources in flask
class CommentView(LessonView):

    def post(self, msg, id, lid, tid):
        app.logger.info('User writing a comment')

        # have to cheese this to make work
        if (msg.isdigit()): # this if for delete
            comment = Comment.query.get(msg)
            db.session.delete(comment)
            db.session.commit()

            flash(u'You have successfully deleted your comment!!', 'success')
            app.logger.info('User deleted their comment')

            return render_template('non_admin/topics/lessons/show.html', lesson=Lesson.query.get(lid),
                                    lid=lid, tid=tid, form=CommentForm(),
                                    back_url=redirect_back('TopicView:index'))
        form = CommentForm()
        if form.validate_on_submit():
            if id != 'new':
                form.iden = int(id)
            # if a new entry create else update
            form.save(True) if msg == 'created' else form.save(False)
            flash(u'You have successfully %s your comment!!' % (msg), 'success')
            app.logger.info('User created or updated a comment')
            return render_template('non_admin/topics/lessons/show.html', lesson=Lesson.query.get(lid),
                                    lid=lid, tid=tid, form=CommentForm(),
                                    back_url=redirect_back('TopicView:index'))

# Inheriting from TopicView is just for naming conventions
# This allows for triple nested resources in flask
class ReplyView(TopicView):
    decorators = [login_required]

    def new(self):
        return 0

    def post(self):
        return 0

    def edit(self):
        return 0

class UserView(FlaskView):
    decorators = [login_required]

    def settings(self):
        app.logger.info('User on settings page')
        return render_template('non_admin/users/settings.html', title='Settings')

    def post(self, id):
        form = UserForm()
        current_user = User.query.get(id)
        form.username.data= current_user.username
        if form.validate_on_submit():
            form.save()
            flash(u'You have successfully udated email', 'success')
            return render_template('non_admin/users/settings.html', title='Settings')

    def edit(self, id):
        # This allows for form data to be filled
        current_user = User.query.get(id)
        form = UserForm()
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.name.data = current_user.name
        form.contact.data = current_user.contact
        return render_template('non_admin/users/edit.html', form=form, msg='updated',
                                id=id, title='Settings')

class BookmarkView(FlaskView):
    decorators = [login_required]

    def index(self):
        app.logger.info('User on bookmark page')

        # I did this like this becuase I didn't want flask-classy to define another route
        page = request.args.get('page', 1, type=int)
        bookmarks = Bookmark.query.paginate(page, 10, False)
        next_url = url_for('BookmarkView:index', page=bookmarks.next_num) \
            if bookmarks.has_next else None
        prev_url = url_for('BookmarkView:index', page=bookmarks.prev_num) \
            if bookmarks.has_prev else None
        return render_template('non_admin/bookmarks/index.html', title='Bookmark',
                                next_url=next_url, prev_url=prev_url,
                                bookmarks=bookmarks.items,
                                back_url=redirect_back('BookmarkView:index'))

    def post(self, msg):
        # have to cheese this to make work
        if (msg.isdigit()): # this if for delete
            bookmark = Bookmark.query.get(msg)
            db.session.delete(bookmark)
            db.session.commit()

            flash(u'You have successfully deleted your bookmark!!', 'success')
            app.logger.info('User deleted a bookmark')

            return render_template('non_admin/bookmarks/index.html', title='Bookmark',
                                    bookmarks=Bookmark.query.all(),
                                    back_url=redirect_back('BookmarkView:index'))

        form = BookmarkForm()
        if form.validate_on_submit():
            # if a new entry create else update
            if (form.save()):
                flash(u'You have successfully saved your bookmark!!', 'success')
                app.logger.info('User created a new bookmark')
                return render_template('non_admin/bookmarks/index.html', title='Bookmark',
                                        bookmarks=Bookmark.query.all(),
                                        back_url=redirect_back('BookmarkView:index'))
            flash(u'You might have already bookmarked this!!!', 'danger')
            app.logger.info('User attempted to bookmark something they already bookmarked')
            return render_template('non_admin/bookmarks/index.html', title='Bookmark',
                                    bookmarks=Bookmark.query.all(),
                                    back_url=redirect_back('BookmarkView:index'))
