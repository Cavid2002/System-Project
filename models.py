from app import db,UserMixin


class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(50),nullable = False,unique = True)
    email = db.Column(db.String(250),nullable = False,unique = True)
    password = db.Column(db.String(250),nullable = False)
    birthdate = db.Column(db.DateTime)
    profile = db.Column(db.String(100))
    folder = db.Column(db.String(100))
    img = db.relationship('Images', backref='user', lazy=True)
    video = db.relationship('Videos',backref='user', lazy=True)

    def save(self):
        db.session.add(self)
        db.session.commit()


class Videos(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    video_path = db.Column(db.String(100))
    comments = db.relationship('Comments',backref = 'videos', lazy = True)
    
    def save(self):
        db.session.add(self)
        db.session.commit()


class Images(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    img_path = db.Column(db.String(100))
    comments = db.relationship('Comments',backref = 'images', lazy = True)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

class Comments(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    video_id = db.Column(db.Integer,db.ForeignKey('videos.id'))
    image_id = db.Column(db.Integer,db.ForeignKey('images.id'))
    user_name = db.Column(db.String(25),nullable = False)
    comment = db.Column(db.Text,nullable = False)

    def save(self):
        db.session.add(self)
        db.session.commit()

db.create_all()



