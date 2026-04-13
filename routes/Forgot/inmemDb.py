import time 
from utils.DB.UpdateDb import EmailSearch
Data={}
def __inputval(email,otp):
    global Data
    Data[email]={"OTP":otp,"ALLOW":int(time.time())+(60*15)}
    
    
def __Validiator(email,otp):
    global Data
    curnt=int(time.time())
    statuscode=400
    if email not in Data:
        return [{"Report":"No Record of that email"},statuscode]
    values= Data[email]
    if values["OTP"]!=otp:
        return [{"Report":"Wrong OTP"},statuscode]
    if values["ALLOW"]<curnt:     
        del Data[email]
        return [{"Report":"Time Exceded"},statuscode]
    statuscode=200
    #Now i need to check the db for the availablity of the users email
    code=EmailSearch(email=email)
    if  isinstance(code,str):
        return [{"Report":f"Thier has been a error:{code}"},statuscode]
    return [{"Report":"go",
             "Codeid":code},statuscode]


def STORAGE(email,otp,action="Create"):
    if action=="Create":
        values=__inputval(email,otp)
        return "go",200
    if action=="Check":
        info=__Validiator(email,otp)
        return info[0],info[1]


