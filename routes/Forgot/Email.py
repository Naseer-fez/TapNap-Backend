from  flask import Blueprint,current_app,request,jsonify
from utils.APIRateLimiter import RequiredRateLimiter
from .CodeGen import OTP
from .inmemDb import STORAGE
FrgEmail=Blueprint("Forgot",__name__)



@FrgEmail.route("/Forgot/<string:email>",methods=["POST","GET"])
@RequiredRateLimiter()
def ForgotEmail(email):
    if request.method=="POST":
        code=OTP(email=email) ##need to send the email
        if code =='E':
            return jsonify({"Report":code}),400
        Data=STORAGE(email=email,otp=code) ## To store the data in memory 
        return jsonify(Data[0]),Data[1]
    else:
        # Data=request.get_json()
        Code=request.headers.get('X-OTP-Code')
        info=STORAGE(email=email,otp=Code,action="Check")
        if(info[1])==400:
            return jsonify(info[0]),info[1]
        return jsonify(info[0]),info[1]

# @FrgEmail.route("/Verify/<string:email>",methods=["GET"])
# @RequiredRateLimiter()
# def Emailcheck(email):
#     

    