from flask_wtf import FlaskForm
from flask import Markup
from wtforms import (StringField,EmailField,PasswordField,SelectField,FileField,DateField,BooleanField)
from wtforms.validators import DataRequired,Length


class LoginForm(FlaskForm):
    email = EmailField(label=Markup('<i class="fa-solid inputIcon fa-envelope"></i>'),
        validators=[DataRequired(),Length(min = 10)])
    passwordLog = PasswordField(label=Markup('<i class="fa-solid inputIcon fa-lock"></i>'),
        validators=[DataRequired()])
    remember = BooleanField(label="Remember me!")


class SignUpForm(FlaskForm):
    username = StringField(label=Markup('<i class="fa-regular inputIcon fa-at"></i>'),
        validators=[DataRequired()])
    email = EmailField(label=Markup('<i class="fa-solid inputIcon fa-envelope"></i>'),
        validators=[DataRequired(),Length(min = 10)])
    password = PasswordField(label=Markup('<i class="fa-solid inputIcon fa-lock"></i>'),
        validators=[DataRequired(),Length(min=8)])
    repassword = PasswordField(label=Markup('<i class="fa-solid inputIcon fa-lock"></i>'),
        validators=[DataRequired(),Length(min=8)])
    birthdate = DateField(label=Markup('<i class="fa-solid inputIcon fa-calendar-days"></i>'),
        validators=[DataRequired()])
 

class UploadMediaForm(FlaskForm):
    file = FileField(label="Add new Post!")
    profile = FileField(label="Change Profile photo")


class PasswordRecoverForm(FlaskForm):
    email = EmailField(validators=[DataRequired()])



class NewPasswordForm(FlaskForm):
    password = PasswordField(validators=[DataRequired(),Length(min=8)])
    repassword = PasswordField(validators=[DataRequired(),Length(min=8)])



class SearchForm(FlaskForm):
    searchBar = StringField(validators=[DataRequired()])


class CommentForm(FlaskForm):
    comment = StringField(validators=[DataRequired()],render_kw={"placeholder": "Enter your comment:"})


class ChangePasswordForm(FlaskForm):
    oldpassword = PasswordField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired(),Length(min=8)])
    repassword = PasswordField(validators=[DataRequired(),Length(min=8)])