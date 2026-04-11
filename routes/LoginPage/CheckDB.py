from models.LoginSql import User,db
import hashlib
from utils.Logger import logs

def Search(username,password):
        info=__checkdb(username=username,password=password)
        Tosend=dict()
        Statuscode=200
        if info[0]==1:
            Tosend={
                "Status":"success",
                "Report":"go",
                "Userid":info[1]
                }        
        else :
            Tosend={
                "Status":"fail",
                "Report":str(info[1]),
                "id":str(-1)}
            Statuscode=400
        
        return Tosend,Statuscode

    
    
    
    
    
    
    
def __checkdb(username,password):
    try:
        Data=User.query.filter_by(Username=username).first()
        if Data:
            hashpass=__Hashing(password)
            if(hashpass==Data.Password):
                return [1,Data.id]
            else:
                return [0,"Invalid password"]
        else:
            return [0,"No user Found"]
    except Exception as e:
        logs(e)


def __Hashing(Password):

    return hashlib.sha256(Password.encode()).hexdigest()
    