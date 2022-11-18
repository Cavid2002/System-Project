from flask import (render_template,redirect,make_response,url_for,flash,request,session,abort,get_flashed_messages)
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import current_user,login_required,login_user,logout_user
from werkzeug.utils import secure_filename
from flask_mail import Message
from app import app,login_manger,mail,media,profile_img
from flask_uploads import UploadNotAllowed
from uuid import uuid4
from datetime import timedelta,datetime
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

def clear_session():
    if('searchedUser' in session):
        session.pop('searchedUser')

    if('email' in session and 'token' in session):
        session.pop('email')
        session.pop('token')        



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
    



@app.route('/sign-up/',methods = ['POST','GET'])
def sign_up():
    sform = SignUpForm()
    if(sform.validate_on_submit()):
        if(sform.password.data != sform.repassword.data):
            flash("Passwords don't macth!","error-message")
        elif(User.query.filter_by(username=sform.username.data).first()):
            flash("Username is already taken!","error-message")
        elif(User.query.filter_by(username=sform.email.data).first()):
            flash("Account with given E-mail already exists!","error-message")
        else:
            user = User(username = sform.username.data,
                        email = sform.email.data,
                        password = generate_password_hash(sform.password.data),
                        folder = generate_string(),
                        profile = 'user-icon.jpg',
                        birthdate = sform.birthdate.data)
            user.save()
            flash("Account was successfully created!","info-message")
            return redirect(url_for('log_in'))
    res = make_response(render_template("sign-up.html",form=sform))
    return res



@app.route('/',methods=['POST','GET'])
@app.route('/log-in/',methods=['POST','GET'])
def log_in():
    clear_session()
    lform = LoginForm()
    if(lform.validate_on_submit()):
        user = User.query.filter_by(email = lform.email.data).first()
        if(user and check_password_hash(user.password, lform.passwordLog.data)):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash("Invalid Password or Email!","error-message")
    res = make_response(render_template('login.html',form = lform))
    return res


@app.route('/logout/',methods=['POST','GET'])
@login_required
def log_out():
    logout_user()
    flash("You logged out","info-message")
    return redirect(url_for('log_in'))



@app.route('/home/',methods=['POST','GET'])
@login_required
def home():
    search_form = SearchForm()
    upload_form = UploadMediaForm()
    
    if(search_form.validate_on_submit()):
        user = User.query.filter_by(username = search_form.searchBar.data).first()
        if(user):
            return redirect(url_for('searched_user_home',username = user.username))
        else:
            flash("User with given name doesn't exists!")
    
    if(upload_form.validate_on_submit() and upload_form.file.data):
        try:
            filename = media.save(storage=upload_form.file.data,folder=current_user.folder,name=generate_string()+".")
            print(filename)
            file = filename.split("/")
            new_file = Media(media_path=file[1],time_added=datetime.utcnow(),user_id=current_user.id)
            new_file.save()
            return redirect(url_for('home'))
        except UploadNotAllowed:
            flash("make sure to upload image or video file!","error-message")
                
    allmedia = Media.query.filter_by(user_id=current_user.id)
    res = make_response(render_template('home.html',form = upload_form,user_info=current_user,images=allmedia,search_form = search_form))
    return res


@app.route('/<username>/home/',methods=['POST','GET'])
@login_required
def searched_user_home(username):
    user = User.query.filter_by(username = username).first()
    allmedia = Media.query.filter_by(user_id = user.id)
    search_form = SearchForm()
    if(search_form.validate_on_submit()):
        us = User.query.filter_by(username = search_form.searchBar.data).first()
        if(us):
            return redirect(url_for('searched_user_home',username = us.username))
        else:
            flash("User with given name doesn't exists!")
    res = make_response(render_template('user-home.html',images = allmedia,search_form = search_form,user_info = user))
    return res
    


@app.route('/profile/',methods=['POST','GET'])
@login_required
def profile():
    upload_form = UploadMediaForm()
    if(upload_form.validate_on_submit()):
        if(upload_form.profile.data):
            if(current_user.profile != "user-icon.jpg"):
                remove("static/uploads/"+current_user.folder + "/" + current_user.profile)
            pfilename = profile_img.save(storage=upload_form.profile.data,folder=current_user.folder,name=generate_string()+".")
            pfile = pfilename.split("/")
            current_user.profile = pfile[1]
            current_user.save()
        if(upload_form.file.data):
            try:
                filename = media.save(storage=upload_form.file.data,folder=current_user.folder,name=generate_string()+".")
                print(filename)
                file = filename.split("/")
                new_file = Media(media_path=file[1],time_added=datetime.utcnow(),user_id=current_user.id)
                new_file.save()
            except UploadNotAllowed:
                flash("Make sure to upload image or video file!","error-message")
        return redirect(url_for('profile'))
    allmedia = Media.query.filter_by(user_id=current_user.id)
    res = make_response(render_template('profile.html',user_info=current_user,images=allmedia,form=upload_form))
    return res


@app.route('/comment/<folder>/<media_path>',methods=['POST','GET'])
@login_required
def comment_section(folder,media_path):
    cform = CommentForm()
    media = Media.query.filter_by(media_path = media_path).first()
    if(not media):
        abort(404)
    if(cform.validate_on_submit()):
        new_comment = Comments(comment=cform.comment.data,
                              media_id = media.id,  
                              user_name=current_user.username,
                              time_added = datetime.utcnow())
        new_comment.save()
        return redirect(url_for('comment_section',folder = folder,media_path = media_path))
    allcomments = Comments.query.filter_by(media_id = media.id)
    res = make_response(render_template('comment-image.html',form=cform,folder = folder,
        media_path=media_path,comments = allcomments))
    return res


@app.route('/password-change/',methods=['POST','GET'])
@login_required
def changepass():
    chform = ChangePasswordForm()
    if(chform.validate_on_submit()):
        if(not check_password_hash(current_user.password, chform.oldpassword.data)):
            flash("Wrong Password","error-message")
        elif(chform.password.data != chform.password.data):
            flash("Passwords don't macth!","error-message")
        else:
            current_user.password = generate_password_hash(chform.password.data)
            flash("Password was successfully changed!","info-message")
            return redirect(url_for("profile"))
    res = make_response(render_template('change-password.html',form = chform))
    return res


@app.route('/recover/',methods=['POST','GET'])
def recover_mail():
    rform = PasswordRecoverForm()
    if(rform.validate_on_submit()):
        em = rform.email.data
        user = User.query.filter_by(email = em).first()
        if(user):
            token = urandom(20).hex()
            session['email'] = em
            session['token'] = token
            msg = Message(f"Email Recovery:",recipients=[em])
            msg.body = f"Email Recovery token is:{url_for('recoverCheck',tk = token, _external = True)} -> Do not share with anyone!\n if it wasn't you ignore this message"
            mail.send(msg)
            flash("Recovery token with instructions was sent to your E-mail!","info-message")
        else:
            flash("User with this email doesn't exists!","error-message")
    res = make_response(render_template("recover-mail.html",form = rform))
    return res


@app.route("/main-recoverpassword/",methods = ['GET','POST'])
@login_required
def recoverpass():
    repassForm = NewPasswordForm()
    if(repassForm.validate_on_submit()):
        if(repassForm.password.data == repassForm.repassword.data):
            current_user.password = generate_password_hash(repassForm.password.data)
            current_user.save()
            flash("Password was successfully changed!","info-message")
            return redirect(url_for("profile"))
        else:
            flash("passwords don't match!","error-message")
    res = make_response(render_template("recover-password.html",form = repassForm))
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


@app.errorhandler(404)
def render404(error):
    res = make_response("<h2>[Error 404]Page not Found!</h2>",404)
    return res