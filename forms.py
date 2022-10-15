from flask_wtf import FlaskForm
from wtforms import StringField,EmailField,PasswordField,SelectField,FileField,DateField,BooleanField
from wtforms.validators import DataRequired,Length


class LoginForm(FlaskForm):
    email = EmailField(label="Enter Email:",validators=[DataRequired(),Length(min = 10)])
    password = PasswordField(label="Enter Password",validators=[DataRequired()])
    remember_user = BooleanField(label="Remember me!")


class SignUpForm(FlaskForm):
    username = StringField(label="Enter Your Username:",validators=[DataRequired()])
    email = EmailField(label="Enter Your Email:",validators=[DataRequired(),Length(min = 10)])
    password = PasswordField(label="Enter Password:",validators=[DataRequired()])
    repassword = PasswordField(label="Renter Password:",validators=[DataRequired()])
    gender = SelectField(label="Enter Your Gender:",validators=[DataRequired()],
                        choices=[("m","MALE"),("f","FEMALE")])
    birthdate = DateField(label="Enter Your Birthdate:",validators=[DataRequired()])
    
class UploadProfile(FlaskForm):
    profile = FileField(label="Enter Profile Photo:")

class UploadPhoto(FlaskForm):
    img = FileField(label="Add new photo:")