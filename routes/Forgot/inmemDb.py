import time 

__Data={}
def __inputval(email,otp):
    global __Data
    __Data[email]={"OTP":otp,"ALLOW":int(time.time())+(60*15)}
    
    
def __Validiator(email,otp):
    curnt=int(time.time())
    statuscode=400
    if email not in __Data:
        return ["No Record of that email",statuscode]
    values= globals()['__Data'][email]
    if values["OTP"]!=otp:
        return ["Wrong OTP",statuscode]
    if values["ALLOW"]<curnt:
        global __Data
        del __Data[email]
        return ["Time Exceded",statuscode]
    statuscode=200
    return "go",statuscode


def STORAGE(email,otp,action="Create"):
    if action=="Create":
        values=__inputval(email,otp)
        return "go",200
    if action=="Check":
        info=__Validiator(email,otp)
        return info[0],info[1]


