from flask import render_template,redirect,make_response,url_for,flash,request,session
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import current_user,login_required,login_user,logout_user
from werkzeug.utils import secure_filename
from flask_mail import Message
from app import app,photos,login_manger,video,mail
from forms import LoginForm,SignUpForm,UploadImage,UploadVideo,PasswordRecoverForm
from flask_uploads import UploadNotAllowed
from uuid import uuid4
from datetime import timedelta
from os import remove,urandom
from models import *


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=5)


@login_manger.user_loader
def load_user(user_id):
    return User.query.filter_by(id = user_id).first()



@app.route("/recover/",methods = ['GET','POST'])
def recover():
    rform = PasswordRecoverForm()
    if(rform.validate_on_submit()):
        em = rform.email.data
        user = User.query.filter_by(email = em).first()
        if(user):
            token = urandom(20).hex()
            session['email'] = em
            session['token'] = token
            msg = Message(f"Email Recovery:",recipients=[em])
            msg.body = f"Email Recovery token is:http://127.0.0.1:5000/recoverinfo/{token} \n Do not share with anyone!\n if it wasn't you ignore this message"
            mail.send(msg)
        else:
            flash("User with this email doesn't exists!")
    res = make_response(render_template("recover.html",form = rform))
    return res

@app.route("/recoverinfo/<tk>")
def recoverCheck(tk):
    if('token' in session and tk == session['token']):
        user = User.query.filter_by(email = session['email']).first()
        login_user(user)
        session.pop('token')
        session.pop('email')
        return redirect(url_for('main'))
    return make_response("<h2>Access Denied</h2>",403)
    
@app.route("/main/images",methods = ['GET','POST'])
@login_required
def main():
    formImg = UploadImage()
    if(formImg.validate_on_submit()):
        if(formImg.profile.data):
            if(current_user.profile != "person-icon.png"):
                remove("static/uploads/"+current_user.folder + "/" + current_user.profile)
            profile = photos.save(storage=formImg.profile.data,folder=current_user.folder)
            splitprofile = profile.split("/")
            current_user.profile = splitprofile[1]
            current_user.save()
        if(formImg.img.data):
            try:
                file = photos.save(storage=formImg.img.data,folder=current_user.folder)
                spiltname = file.split("/")
                new_img = Images(img_path=spiltname[1],user_id=current_user.id)
                new_img.save()
            except UploadNotAllowed:
                flash("Make sure to upload Image file") 
        return redirect(url_for('main'))
    userImg = Images.query.filter_by(user_id = current_user.id)
    res = make_response(render_template("mainImg.html",user_info = current_user,form = formImg,images = userImg))
    return res


@app.route("/main/videos",methods = ['POST','GET'])
@login_required
def videos():
    formVideo = UploadVideo()
    if(formVideo.validate_on_submit()):
        if(formVideo.profile.data):
            if(current_user.profile != "person-icon.png"):
                remove("static/uploads/"+current_user.folder + "/" + current_user.profile)
            profile = photos.save(storage=formVideo.profile.data,folder=current_user.folder)
            splitprofile = profile.split("/")
            current_user.profile = splitprofile[1]
            current_user.save()
            
        if(formVideo.video.data):
            try:
                file = video.save(storage = formVideo.video.data,folder=current_user.folder)
                spiltname = file.split("/")
                new_video = Videos(video_path=spiltname[1],user_id=current_user.id)
                new_video.save()
            except UploadNotAllowed:
                flash("Make sure to upload Video file!")
        return redirect(url_for('videos'))
    userVid = Videos.query.filter_by(user_id = current_user.id)
    res = make_response(render_template("mainVideos.html",user_info = current_user,form = formVideo,vids = userVid))
    return res


@app.route('/login/',methods = ['GET','POST'])
def logIn():
    logform = LoginForm()
    if(logform.validate_on_submit()):
        user = User.query.filter(User.email == logform.email.data).first()
        if(user and check_password_hash(user.password,logform.password.data)):
            login_user(user,remember=logform.remember_user.data)
            return redirect(url_for("main"))
        else:
            flash("Invalid Email or Password!")
    res = make_response(render_template("login.html",form = logform))
    return res




@app.route("/sign-up/",methods = ['GET','POST'])
def signUp():
    signForm = SignUpForm()
    if(signForm.validate_on_submit()):
        if(signForm.password.data == signForm.repassword.data):
            usr = User.query.filter_by(email = signForm.email.data).first()
            if(not usr):
                folderID = str(uuid4())
                default_img = "person-icon.png"
                new_user = User(
                    username = signForm.username.data,
                    email = signForm.email.data,
                    password = generate_password_hash(signForm.password.data),
                    gender = signForm.gender.data,
                    birthdate = signForm.birthdate.data,
                    profile = default_img,
                    folder = folderID
                )
                new_user.save()
                return redirect(url_for("logIn"))
            else:
                flash("User with this E-mail already exists!")
        else:
            flash("Passwords don't match!")
    res = make_response(render_template("sign-up.html",form = signForm),200)
    return res



@app.route("/logout/")
@login_required
def logOut():
    logout_user()
    return redirect(url_for('logIn'))


@app.errorhandler(404)
def render404(error):
    res = make_response("<h2>[Error 404]Page not Found!</h2>",404)
    return res

