from app import db,UserMixin


class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(50),nullable = False)
    gender = db.Column(db.String(1),nullable = False)
    email = db.Column(db.String(250),nullable = False,unique = True)
    password = db.Column(db.String(250),nullable = False)
    birthdate = db.Column(db.DateTime)
    profile = db.Column(db.String(100))


    def save(self):
        db.session.add(self)
        db.session.commit()


db.create_all()