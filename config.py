from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager,UserMixin
from flask_uploads import IMAGES, UploadSet, configure_uploads
from app import app



def get_access_to_db():
    file = open(".db",'r')
    res = file.readline()
    file.close()
    return res


app.config['UPLOADED_IMG_DEST'] = "uploads/"
app.config['SQLALCHEMY_DATABASE_URI'] = get_access_to_db()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '0bd82f50a17b43654c84ab57a32d54aaec71f88dbee356e1a5'


login_manger = LoginManager()
login_manger.init_app(app)

db = SQLAlchemy(app)
migrate = Migrate(app,db)


photos = UploadSet("img", IMAGES)
configure_uploads(app,photos)