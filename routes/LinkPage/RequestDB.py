import hashlib
from models.LinksTable import Links,db
import time
import threading
from utils.Logger import logs
# from app import app
from utils.DB.RemoveData import OldData
def Getlink(Code,Password):
        info=__Searchdb(Cde=Code,pwd=Password)
        TOsend={}
        if info[0]==1:
            Tosend={
                "Status":"success",
                "Report":"go",
                "LINK":info[1]
                } 
            Statuscode=200
        else:   
            Tosend={
            "Status":"fail",
            "Report":str(info[1]),
            "LINK":str(-1)}
            Statuscode=400

        
        return Tosend,Statuscode

    



def __Searchdb(Cde,pwd):
        pwd=__Hashing(pwd)
        try:
            
            Data=Links.query.filter_by(Code=Cde).first()    
            if Data:
                if Data.Password is None:
                    pass
                elif pwd!=Data.Password:
                    return [0,"Wrong Password"]
                if((__Timevaladation(Data=Data))is False):
                    # print("HAHHA")
                    return [0,"Invalid Code or Time Limit "]

                Tosend=Data.Link
                return [1,Tosend]
            else:
                return [0,"Wrong Code Entred"]
        except Exception as e:
            logs(message= e)
            return [-1,e]





def __Timevaladation(Data):
        crttime=int(time.time())

        if Data.AllowedTime<crttime:
            # thread = threading.Thread(target=OldData,args=(Data,),daemon=True)
            # thread.start()
            OldData(Data)
            return False
        else :
            # print("WOWOOW")
            return True


def __Hashing(Password):
    if Password is None:
        return
    return hashlib.sha256(Password.encode()).hexdigest()
    
