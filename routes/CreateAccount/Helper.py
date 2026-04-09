import hashlib
import base64
import uuid
from models.LoginSql import db,User
from sqlalchemy.exc import IntegrityError
from utils.Logger import logs

# class User(db.Model):
#     __tablename__="User"
#     id = db.Column(db.Integer, primary_key=True,unique=True,autoincrement=True)
#     Username=db.Column(db.String(50),nullable=False,unique=True)
#     Password=db.Column(db.String(256),nullable=False)
#     Email=db.Column(db.String(50),nullable=True,unique=True)
#     links = db.relationship('Links', backref='owner', lazy=True)

def CreateAccount(username,password,email):
    info=__TransferingDB(username=username,password=password,email=email)
    Tosend=dict()
    Statuscode=200
    Tosend=dict()
    Statuscode=200
    if info[0]==1:
        Tosend={
            "Status":"success",
            "Report":"go",
            "Codeid":info[1]
            }        
    else :
        Tosend={
            "Status":"fail",
            "Report":str(info[1]),
            "Codeid":str(-1)}
        Statuscode=400
    return Tosend,Statuscode



def __TransferingDB(username,password,email):
        password=__Hashing(Password=password) #Not gonna show in this repo for safety 
        Data=User(Username=username,Password=password,Email=email)
        try:
            db.session.add(Data)
            db.session.commit()
        except IntegrityError:
            
            db.session.rollback()
            return [-1,"The user Already Exist"]
        
        except Exception as e:
            # print("HEre")
            db.session.rollback()
            ##Log this 
            logs(message=e)
            return [0,e]
        Userid=Data.id
        return [1,Userid]

   
def __Hashing(Password):
    return hashlib.sha256(Password.encode()).hexdigest()


if __name__=="__main__":
    print(__Hashing("HEllo"))


