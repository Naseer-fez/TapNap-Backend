from  flask import Blueprint,current_app,request,jsonify
from utils.APIRateLimiter import RequiredRateLimiter
from .Authecation import Lookonce

Chnagepass=Blueprint("Paswordchg",__name__)



@Chnagepass.route("/Verify",methods=["POST"])
def Passwordchange():
    Data=request.get_json()
    info=Lookonce(Data)
    return jsonify(info[0]),info[1]