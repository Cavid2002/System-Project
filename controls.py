from flask import render_template,redirect,make_response,url_for,flash
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename
from config import migrate,app,photos
from forms import LoginForm,SignUpForm
from uuid import uuid4
from models import *


@app.route("/main")
def main():
    res = make_response(url_for("main.html"))
    return res

@app.route("/login/",methods = ['GET','POST'])
def logIn():
    logform = LoginForm()
    if(logform.validate_on_submit()):
        user = User.query.filter(User.email == logform.email.data).first()
        if(user and check_password_hash(user.password,logform.password.data)):
            return redirect(url_for("main"))
        else:
            flash("Invalid Email or Password!")
    res = make_response(render_template("login.html",form = logform),200)
    return res


@app.route("/sign-up/")
def signUp():
    signForm = SignUpForm()
    if(signForm.validate_on_submit()):
        if(signForm.password.data == signForm.repassword.data):
            file = photos.save(storage = signForm.profile.data)
            fn = uuid4() + secure_filename(file.filename)
            new_user = User(
                username = signForm.username.data,
                password = generate_password_hash(signForm.password.data),
                gender = signForm.gender.data,
                birthdate = signForm.birthdate.data,
                profile = signForm.profile.data
            )
            new_user.save()
            return redirect(url_for("/login"))
        else:
            flash("Passwords don't match!")
    res = make_response(render_template("sign-up.html",form = signForm))
    return res


@app.errorhandler(404)
def render404(error):
    res = make_response("<h2>[INFO] -->[Error 404]Page not Found!</h2>",404)
    return res

