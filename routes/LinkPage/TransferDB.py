from models.LinksTable import Links,db
from sqlalchemy.exc import IntegrityError
import time 
import hashlib
    # ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # UserId=db.Column(db.Integer, db.ForeignKey('User.id'),index=True, nullable=True,default=-1)
    # Link=db.Column(db.String(768),unique=True,nullable=False)
    # Password=db.Column(db.String(256),nullable=True)
    # Code=db.Column(db.Integer,unique=True,nullable=False)
    # CreatedTime= db.Column(db.BigInteger, default=lambda: int(time.time()),nullable=False)
    # AllowedTime=db.Column(db.BigInteger, default=lambda: int(time.time())+864001,nullable=False)

def Gateway(UserData:dict):
    UserData=__DataProcessing(UserData)
    info=__Todb(UserData=UserData)
    # print(UserData)
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


def __DataProcessing(UserData:dict)->dict:
    tim=int(time.time())  
    UserData["Crttime"]=tim
    UserData["AldTime"]=tim+864001
    if UserData["Password"] is not None:
        UserData["Password"]=__Hashing(UserData["Password"])

    
    return UserData

def __Hashing(Password):
    return hashlib.sha256(Password.encode()).hexdigest()



def __Todb(UserData:dict):

    Data=Links(UserId=UserData["Userid"],Link=UserData["Link"],Password=UserData["Password"],
               Code=UserData["Code"],CreatedTime=UserData["Crttime"],AllowedTime=UserData["AldTime"])
    try:
        db.session.add(Data)
        db.session.commit()
    except IntegrityError:
            db.session.rollback()
            return [-1,"The Code Already Exist "]
        
    except Exception as e:
            db.session.rollback()
            ##Log this 
            return [0,e]
    Codeid=Data.ID
    return [1,Codeid]