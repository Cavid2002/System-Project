from app import db,UserMixin


class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(50),nullable = False,unique = True)
    email = db.Column(db.String(250),nullable = False,unique = True)
    password = db.Column(db.String(250),nullable = False)
    birthdate = db.Column(db.DateTime)
    profile = db.Column(db.String(100))
    folder = db.Column(db.String(100))
    media = db.relationship('Media', backref='user', lazy=True)
    like = db.relationship('Likes', backref='user', lazy=True)
    def save(self):
        db.session.add(self)
        db.session.commit()



class Media(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    media_path = db.Column(db.String(100))
    time_added = db.Column(db.DateTime)
    comments = db.relationship('Comments',backref = 'media', lazy = True)
    like = db.relationship('Likes', backref='media', lazy=True)
    def save(self):
        db.session.add(self)
        db.session.commit()



class Comments(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    media_id = db.Column(db.Integer,db.ForeignKey('media.id'))
    time_added = db.Column(db.DateTime)
    user_name = db.Column(db.String(25),nullable = False)
    comment = db.Column(db.Text,nullable = False)

    def save(self):
        db.session.add(self)
        db.session.commit()


class Likes(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    media_id = db.Column(db.Integer,db.ForeignKey('media.id'))

db.create_all()



