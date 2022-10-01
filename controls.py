from flask import render_template,redirect,make_response,url_for,flash
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import current_user,login_required,login_user,logout_user
from werkzeug.utils import secure_filename
from app import migrate,app,photos,login_manger
from forms import LoginForm,SignUpForm,UploadPhoto
from uuid import uuid4
from models import *


@login_manger.user_loader
def load_user(user_id):
    return User.query.filter_by(id = user_id).first()


@login_required
@app.route("/main",methods = ['GET','POST'])
def main():
    form = UploadPhoto()
    if(form.validate_on_submit()):
        file = photos.save(storage=form.img.data,folder=current_user.folder)
    res = make_response(render_template("main.html",user_info = current_user))
    return res

@app.route("/login",methods = ['GET','POST'])
def logIn():
    logform = LoginForm()
    if(logform.validate_on_submit()):
        user = User.query.filter(User.email == logform.email.data).first()
        if(user and check_password_hash(user.password,logform.password.data)):
            login_user(user)
            return redirect(url_for("main"))
        else:
            flash("Invalid Email or Password!")
    res = make_response(render_template("login.html",form = logform),200)
    return res


@app.route("/sign-up",methods = ['GET','POST'])
def signUp():
    signForm = SignUpForm()
    if(signForm.validate_on_submit()):
        if(signForm.password.data == signForm.repassword.data):
            usr = User.query.filter_by(email = signForm.email.data)
            if(usr != None):
                newid = str(uuid4())
                new_user = User(
                    username = signForm.username.data,
                    email = signForm.email.data,
                    password = generate_password_hash(signForm.password.data),
                    gender = signForm.gender.data,
                    birthdate = signForm.birthdate.data,
                    folder = newid
                )
                new_user.save()
                return redirect(url_for("logIn"))
            else:
                flash("User with this E-mail already exists!")
        else:
            flash("Passwords don't match!")
    res = make_response(render_template("sign-up.html",form = signForm))
    return res


@app.route("/logout")
@login_required
def logOut():
    logout_user()
    return redirect(url_for('logIn'))


@app.errorhandler(404)
def render404(error):
    res = make_response("<h2>[Error 404]Page not Found!</h2>",404)
    return res

