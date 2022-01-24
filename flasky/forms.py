from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flasky.models import User
from flask_login import current_user

class registration_form(FlaskForm):
    
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if(user):
            raise ValidationError('That username already exists. Please choose another one.')

    def validate_email(self, email):
        user = User.query.filter_by(username=email.data).first()
        if(user):
            raise ValidationError('That email is already taken. Do you already have an account?')


class login_form(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class update_account_form(FlaskForm):

    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if(username.data != current_user.username):
            user = User.query.filter_by(username=username.data).first()
            if(user):
                raise ValidationError('That username already exists. Please choose another one.')

    def validate_email(self, email):
        if(email.data != current_user.email):
            user = User.query.filter_by(username=email.data).first()
            if(user):
                raise ValidationError('That email is already taken. Do you already have an account?')


class post_form(FlaskForm):

    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


class request_reset_form(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if(not user):
            raise ValidationError("There isn't an account associated with that email")

class reset_pass_form(FlaskForm):

    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')