from flask import (render_template,redirect,make_response,url_for,flash,request,session,abort,get_flashed_messages)
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import current_user,login_required,login_user,logout_user
from werkzeug.utils import secure_filename
from flask_mail import Message
from app import app,photos,login_manger,video,mail
from flask_uploads import UploadNotAllowed
from uuid import uuid4
from datetime import timedelta
from os import remove,urandom
from string import ascii_letters,digits
from random import choice
from models import *
from forms import *



def generate_string(size: int = 15) -> str:
    symbols = ascii_letters + digits
    result = ""
    for i in range(size):
        result += choice(symbols)
    return result

 

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=5)

# @app.after_request
# def clear_session():
#     ...

@login_manger.user_loader
def load_user(user_id):
    return User.query.filter_by(id = user_id).first()
    



@app.route('/main/search',methods = ['GET','POST'])
def search():
    sform = SearchForm()
    if(sform.validate_on_submit()):
        user = User.query.filter_by(username = sform.inputdata.data).first()
        session["searchedUser"] = user.id
        return redirect(url_for('foundUserImage'))
    res = make_response(render_template("search.html",form = sform))
    return res


@app.route('/user-images/')
@login_required
def foundUserImage():
    user = User.query.filter_by(id = session['searchedUser']).first()
    images = Images.query.filter_by(user_id = user.id)
    res = make_response(render_template('user-img.html',user_info = user,images = images))
    return res


@app.route('/user-videos/')
@login_required
def foundUserVideo():
    user = User.query.filter_by(id = session['searchedUser']).first()
    vids = Videos.query.filter_by(user_id = user.id)
    res = make_response(render_template('user-video.html',user_info = user,vids = vids))
    return res



@app.route("/recover/",methods = ['GET','POST'])
def recover():
    rform = PasswordRecoverForm()
    if(rform.validate_on_submit()):
        em = rform.email.data
        user = User.query.filter_by(email = em).first()
        if(user):
            token = urandom(20).hex()
            ipadd = '198.168.0.109'
            session['email'] = em
            session['token'] = token
            msg = Message(f"Email Recovery:",recipients=[em])
            msg.body = f"Email Recovery token is:http://{ipadd}/recoverinfo/{token} -> Do not share with anyone!\n if it wasn't you ignore this message"
            mail.send(msg)
        else:
            flash("User with this email doesn't exists!")
    res = make_response(render_template("recover-mail.html",form = rform))
    return res


@app.route("/recoverinfo/<tk>")
def recoverCheck(tk):
    if('token' in session and tk == session['token']):
        user = User.query.filter_by(email = session['email']).first()
        login_user(user)
        session.pop('token')
        session.pop('email')
        return redirect(url_for('recoverpass'))
    return make_response("<h2>Access Denied</h2>",403)


    
@app.route("/main-recoverpassword/",methods = ['GET','POST'])
@login_required
def recoverpass():
    repassForm = NewPasswordForm()
    if(repassForm.validate_on_submit()):
        if(repassForm.password.data == repassForm.repassword.data):
            current_user.password = generate_password_hash(repassForm.password.data)
            current_user.save()
            return redirect(url_for("main"))
        else:
            flash("passwords don't match!")
    res = make_response(render_template("recover-password.html",form = repassForm))
    return res


@app.route('/main-changepassword/',methods = ['GET','POST'])
@login_required
def changepass():
    changepassform = ChangePasswordForm()
    if(changepassform.validate_on_submit()):
        if(not check_password_hash(current_user.password, changepassform.oldpassword.data)):
            flash("Wrong user password!")
        elif(changepassform.password.data != changepassform.repassword.data):
            flash("Passwords don't match!")
        else:
            current_user.password = generate_password_hash(changepassform.password.data)
            current_user.save()
            return redirect(url_for('main'))
    res = make_response(render_template('change-password.html',form = changepassform))
    return res



@app.route("/main-images/",methods = ['GET','POST'])
@login_required
def main():
    if('searchedUser' in session):
        session.pop('searchedUser')
    formImg = UploadImage()
    if(formImg.validate_on_submit()):
        if(formImg.profile.data):
            if(current_user.profile != "person-icon.png"):
                remove("static/uploads/"+current_user.folder + "/" + current_user.profile)
            profile = photos.save(storage=formImg.profile.data,folder=current_user.folder,name=generate_string()+".")
            splitprofile = profile.split("/")
            current_user.profile = splitprofile[1]
            current_user.save()
        if(formImg.img.data):
            try:
                file = photos.save(storage=formImg.img.data,folder=current_user.folder,name=generate_string()+".")
                spiltname = file.split("/")
                new_img = Images(img_path=spiltname[1],user_id=current_user.id)
                new_img.save()
            except UploadNotAllowed:
                flash("Make sure to upload Image file!") 
        return redirect(url_for('main'))
    userImg = Images.query.filter_by(user_id = current_user.id)
    res = make_response(render_template("my-img.html",user_info = current_user,form = formImg,images = userImg))
    return res



@app.route("/main-videos/",methods = ['POST','GET'])
@login_required
def videos():
    formVideo = UploadVideo()
    if(formVideo.validate_on_submit()):
        if(formVideo.profile.data):
            if(current_user.profile != "person-icon.png"):
                remove("static/uploads/"+current_user.folder + "/" + current_user.profile)
            profile = photos.save(storage=formVideo.profile.data,folder=current_user.folder,name=generate_string()+".")
            splitprofile = profile.split("/")
            current_user.profile = splitprofile[1]
            current_user.save()
            
        if(formVideo.video.data):
            try:
                file = video.save(storage = formVideo.video.data,folder=current_user.folder,name=generate_string()+".")
                spiltname = file.split("/")
                new_video = Videos(video_path=spiltname[1],user_id=current_user.id)
                new_video.save()
            except UploadNotAllowed:
                flash("Make sure to upload Video file!")
        return redirect(url_for('videos'))
    userVid = Videos.query.filter_by(user_id = current_user.id)
    res = make_response(render_template("my-video.html",user_info = current_user,form = formVideo,vids = userVid))
    return res



@app.route("/logout/")
@login_required
def logOut():
    logout_user()
    return redirect(url_for('logIn'))


@app.route('/',methods = ['GET','POST'])
@app.route('/login/',methods = ['GET','POST'])
def logIn():
    logform = LoginForm()
    if(logform.validate_on_submit()):
        user = User.query.filter(User.email == logform.email.data).first()
        if(user and check_password_hash(user.password,logform.passwordLog.data)):
            login_user(user,remember=logform.remember.data)
            return redirect(url_for("main"))
        else:
            flash("Invalid Email or Password!")
    res = make_response(render_template("login.html",form = logform))
    return res


@app.route("/comment-image/<username>/<image_path>",methods = ['GET','POST'])
@login_required
def comment_section_img(image_path,username):
    image = Images.query.filter_by(img_path = image_path).first()
    user = User.query.filter_by(username = username).first()
    if(not user or not image):
        abort(404)
    allcomments = Comments.query.filter_by(image_id = image.id)
    cform = CommentForm()
    if(cform.validate_on_submit()):
        new_comment = Comments(
            image_id = image.id,
            comment = cform.comment.data,
            user_name = current_user.username)
        new_comment.save()
        return redirect(url_for('comment_section_img',username = username,image_path = image_path))
    
    res = make_response(render_template("comment-image.html",form = cform,img = image_path,folder = user.folder,comments = allcomments))
    return res



@app.route("/comment-video/<username>/<video_path>",methods = ['GET','POST'])
@login_required
def comment_section_video(username,video_path):
    video = Videos.query.filter_by(video_path = video_path).first()
    user = User.query.filter_by(username = username).first()
    if(not user or not video):
        abort(404)
    allcomments = Comments.query.filter_by(video_id = video.id)
    cform = CommentForm()
    if(cform.validate_on_submit()):
        new_comment = Comments(
            video_id = video.id,
            comment = cform.comment.data,
            user_name = current_user.username)
        new_comment.save()
        return redirect(url_for('comment_section_video',username = username,video_path = video_path))
    res = make_response(render_template("comment-video.html",form = cform,video_path = video_path,folder = user.folder,comments = allcomments))
    return res



@app.route("/sign-up/",methods = ['GET','POST'])
def signUp():
    signForm = SignUpForm()
    if(signForm.validate_on_submit()):
        if(signForm.password.data == signForm.repassword.data):
            usr_em = User.query.filter_by(email = signForm.email.data).first()
            usr_name = User.query.filter_by(username = signForm.username.data).first()
            if(usr_name):
                flash("Username is already taken!")
            elif(usr_em):
                flash("User with this E-mail already exists!")
            else:
                folderID = generate_string(20)
                default_img = "person-icon.png"
                new_user = User(
                    username = signForm.username.data,
                    email = signForm.email.data,
                    password = generate_password_hash(signForm.password.data),
                    birthdate = signForm.birthdate.data,
                    profile = default_img,
                    folder = folderID
                )
                new_user.save()
                return redirect(url_for("logIn"))
        else:
            flash("Passwords don't match!")
    res = make_response(render_template("sign-up.html",form = signForm),200)
    return res



@app.errorhandler(404)
def render404(error):
    res = make_response("<h2>[Error 404]Page not Found!</h2>",404)
    return res
