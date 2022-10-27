from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager,UserMixin
from flask_uploads import IMAGES, UploadSet, configure_uploads
from flask_mail import Mail
import os


def get_access_to_db():
    file = open("database.txt",'r')
    res = file.readline()
    file.close()
    return res


def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    
    app.config['UPLOADED_IMG_DEST'] = "static/uploads/"
    app.config['UPLOADED_VIDEO_DEST'] = "static/uploads/"
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    
    app.config['MAIL_SERVER'] = "smtp.gmail.com"
   
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = "mygalerynoreply@gmail.com"
    app.config['MAIL_PASSWORD'] = os.environ.get('PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = "mygalerynoreply@gmail.com"
    app.config['MAIL_MAX_EMAILS'] = 2
    app.config['MAIL_ASCII_ATTACHMENTS'] = False
    
    
    return app

app = create_app()

login_manger = LoginManager()
login_manger.login_view = "logIn"
login_manger.login_message = "You are not logged in!"
login_manger.session_protection = "strong"
login_manger.init_app(app)


db = SQLAlchemy(app)
migrate = Migrate(app,db)


mail = Mail(app)

video = UploadSet("video",('mov','mp4'))
photos = UploadSet("img", IMAGES)
configure_uploads(app, video)
configure_uploads(app,photos)


from controls import *

if(__name__ == "__main__"):
    app.run(debug = True)


#lzlunpqltjpuqvbs