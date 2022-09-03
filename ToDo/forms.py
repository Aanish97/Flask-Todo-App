from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField
from wtforms.fields.datetime import DateField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField


# Create Login Form
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Create a Posts Form
class TodoForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    note = CKEditorField('Note', validators=[DataRequired()])
    due_date = DateField("Due Date", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Create a Register Form Class
class UserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     EqualTo('confirm_password', message='Passwords Must Match!')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])

