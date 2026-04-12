from  flask import Blueprint,current_app,request,jsonify
from utils.APIRateLimiter import RequiredRateLimiter
from .CodeGen import OTP
from .inmemDb import STORAGE
FrgEmail=Blueprint("Forgot",__name__)



@FrgEmail.route("/Forgot/<String:email>",methods=["POST"])
@RequiredRateLimiter()
def ForgotEmail(email):
    code=OTP(email=email) ##need to send the email
    Data=STORAGE(email=email,otp=code,)
    return jsonify(Data[0]),Data[1]

@FrgEmail.route("/Verify/<String:email>",methods=["GET"])
@RequiredRateLimiter()
def Emailcheck(email):
    Data=request.get_json()
    Code=Data.get("code")
    info=STORAGE(email=email,otp=Code,action="Check")
    if(info[1])==400:
        return jsonify(info[0]),info[1]
    # Now give the access
    
    