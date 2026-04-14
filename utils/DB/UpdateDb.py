from models.LoginSql import db,User
from utils.Logger import logs

# class User(db.Model):
#     __tablename__="User"
#     id = db.Column(db.Integer, primary_key=True,unique=True,autoincrement=True)
#     Username=db.Column(db.String(50),nullable=False,unique=True)
#     Password=db.Column(db.String(256),nullable=False)
#     Email=db.Column(db.String(50),nullable=True,unique=True)
#     links = db.relationship('Links', backref='owner', lazy=True)
    


def EmailSearch(email):
    
    try:
        Data=User.query.filter_by(Email=email).first()
    except Exception as e:
        db.session.rollback()
        logs(e)
        # print(e)
        return f"e"
    if Data is None:
        return "User Not Found!!!"
    return Data.id



def updateinfo(id,item):
    Data=User.query.filter_by(id=id).first()
    if Data is None:
        return "User not Found"
    Data.item=item
    try:
        db.session.commit()
        return Data.Id
    except Exception as e:
        db.session.rollback()
        logs(e)
        return str(e)
    