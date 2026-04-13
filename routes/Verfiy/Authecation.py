from models.LoginSql import User,db
from utils.DB.UpdateDb  import updateinfo
from routes.CreateAccount.Helper import __Hashing



def Lookonce(Data):
    Id=Data.get("id")
    Password=__Hashing(Data.get("password"))
    info=updateinfo(id=Id,item=Password)
    tosend={}
    statuscode=400
    if isinstance(info,str):
        tosend={
            "Report":f"{info}",
            "Code":-1
            }
    else:
        statuscode=200
        tosend={
            "Report":"go",
            "Code":info
            
        }
    return tosend,statuscode