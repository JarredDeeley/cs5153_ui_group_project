from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_ckeditor import CKEditorField
from app.models import *
from app import db

class SearchForm(FlaskForm):
    search = StringField('search', validators=[DataRequired()])

# Login form in templates/login.html
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')

# Topics form in templates/admin/topics/edit|new.html
class TopicForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    text = CKEditorField('Text', validators=[DataRequired()])
    # This is only used for edit. So dont add valiations
    iden = HiddenField('Topic ID')

    # The save method first check if on new or edit page
    # based off that deterime whether to create or update
    def save(self, new):
        if new:
            topic = Topic(name=self.name.data,description=self.description.data,text=self.text.data)
            db.session.add(topic)
        else:
            topic = Topic.query.get(self.iden.data)
            topic.name = self.name.data
            topic.description = self.description.data
            topic.text = self.text.data
        db.session.commit()

# Lessons form in templates/admin/lessons/edit|new.html
class LessonForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    text = CKEditorField('Text', validators=[DataRequired()])
    tidf = HiddenField('Topic ID', validators=[DataRequired()])
    # This is only used for edit. So dont add valiations
    iden = HiddenField('Lesson ID')

    # The save method first check if on new or edit page
    # based off that deterime whether to create or update
    def save(self, new):
        if new:
            lesson = Lesson(name=self.name.data,description=self.description.data,
                            text=self.text.data,topic_id=self.tidf.data)
            db.session.add(lesson)
        else:
            lesson = Lesson.query.get(self.iden.data)
            lesson.topic_id = self.tidf.data
            lesson.name = self.name.data
            lesson.description = self.description.data
            lesson.text = self.text.data
        db.session.commit()

# Comments form in templates/non-admin/lessons/edit|new.html
class CommentForm(FlaskForm):
    text = TextAreaField('Text', validators=[DataRequired()])
    lidf = HiddenField('Lesson ID', validators=[DataRequired()])
    uidf = HiddenField('User ID', validators=[DataRequired()])

    # This is only used for edit. So dont add valiations
    iden = HiddenField('Comment ID')

    # The save method first check if on new or edit page
    # based off that deterime whether to create or update
    def save(self, new):
        if new:
            comment = Comment(text=self.text.data,lesson_id=self.lidf.data,user_id=self.uidf.data)
            db.session.add(comment)
        else:
            comment = Comment.query.get(self.iden)
            comment.lesson_id = self.lidf.data
            comment.user_id = self.uidf.data
            comment.text = self.text.data
        db.session.commit()

class BookmarkForm(FlaskForm):
    uidf = HiddenField('User ID', validators=[DataRequired()])
    tidf = HiddenField('Topic ID', validators=[DataRequired()])
    lidf = HiddenField('Lesson ID')

    def save(self):
        ret = False
        if db.session.query(Bookmark.id).filter_by(
                            user_id=self.uidf.data,topic_id=self.tidf.data,
                            lesson_id=self.lidf.data).scalar() is None:
            bookmark = Bookmark(user_id=self.uidf.data,topic_id=self.tidf.data,lesson_id=self.lidf.data)
            db.session.add(bookmark)
            db.session.commit()
            ret = True
        return ret

# Roles form in folder templates/admin/roles/new|edit.html
class RoleForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    # This is only used for edit. So dont add valiations
    iden = HiddenField('Role ID')

    # The save method first check if on new or edit page
    # based off that deterime whether to create or update
    def save(self, new):
        if new:
            role = Role(name=self.name.data,description=self.description.data)
            db.session.add(role)
        else:
            role = Role.query.get(self.iden.data)
            role.name = self.name.data
            role.description = self.description.data
        db.session.commit()

# This may change or we can add an account form
# User form locate templates/admin/users/edit.html
class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Name', validators=[])
    contact = StringField('Contact', validators=[])
    # This is only used for edit. So dont add valiations
    iden = HiddenField('User ID')

    # The save method first check if on new or edit page
    # based off that deterime whether to create or update
    def save(self):
        user = User.query.get(self.iden.data)
        user.email = self.email.data
        user.username = self.username.data
        user.name = self.name.data
        user.contact = self.contact.data
        db.session.commit()

# Register Form in templates/register.html
class RegistrationForm(FlaskForm):
    remember_me = BooleanField('Remember Me')
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    recaptcha = RecaptchaField()
    submit = SubmitField('Register')

    def save(self):
        user = User(username=self.username.data, email=self.email.data)
        user.set_password(self.password.data)
        db.session.add(user)
        db.session.commit()

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
