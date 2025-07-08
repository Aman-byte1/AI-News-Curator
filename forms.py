from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from models import User

class RegistrationForm(FlaskForm):
    """
    Form for user registration.
    """
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        """Checks if a username already exists."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        """Checks if an email already exists."""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    """
    Form for user login.
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class NewsArticleForm(FlaskForm):
    """
    Form for media users to create/edit news articles.
    """
    title = StringField('Article Title', validators=[DataRequired(), Length(min=5, max=255)])
    content = TextAreaField('Article Content', validators=[DataRequired()])
    category = StringField('Category (e.g., Politics, Tech, Sports)', validators=[Length(max=100)])
    source_name = StringField('Source Name (e.g., Reuters, BBC)', validators=[Length(max=100)])
    source_url = StringField('Original Source URL', validators=[Length(max=500)])
    submit = SubmitField('Post Article')