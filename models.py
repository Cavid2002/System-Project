from app import db,UserMixin


class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(50),nullable = False)
    gender = db.Column(db.String(1),nullable = False)
    email = db.Column(db.String(250),nullable = False,unique = True)
    password = db.Column(db.String(250),nullable = False)
    birthdate = db.Column(db.DateTime)
    profile = db.Column(db.String(100))
    folder = db.Column(db.String(100))
    img = db.relationship('Images', backref='user', lazy=True)
    comments = db.relationship('Comments',backref = 'user', lazy = True)


    def save(self):
        db.session.add(self)
        db.session.commit()


class Images(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    img_path = db.Column(db.String(100))
    
    
    def save(self):
        db.session.add(self)
        db.session.commit()

class Comments(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    comment = db.Column(db.Text,nullable = False)

    def save(self):
        db.session.add(self)
        db.session.commit()

db.create_all()