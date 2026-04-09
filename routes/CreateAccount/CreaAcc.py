from flask import Blueprint,jsonify,request
from utils.APIRateLimiter import RequiredRateLimiter
from .Helper import CreateAccount
CreatBp=Blueprint("Create",__name__)


@CreatBp.route("/Register",methods=["POST"])
@RequiredRateLimiter()
def CreationPage():
    Data=request.get_json()
    UserName=Data.get("username")
    Password=Data.get("password")
    Email=Data.get("email")
    info=CreateAccount(username=UserName,password=Password,email=Email)
    return jsonify(info[0]),info[1]
    # Tosend={
    #         "Status":"Fail",
    #         "Report":str("GO"),
    #         "Userid":-1}
    # return jsonify(Tosend), 200

