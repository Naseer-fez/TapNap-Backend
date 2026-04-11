from flask import Blueprint,jsonify,request
from utils.APIRateLimiter import RequiredRateLimiter
from .CheckDB import Search
LoginBP=Blueprint("Login",__name__)

@LoginBP.route("/Login",methods=["POST","GET"])
@RequiredRateLimiter()
def LoginPage():
    Data=request.get_json()
    usernmae=Data.get("username")
    password=Data.get("password")
    info=Search(username=usernmae,password=password)
    return info[0],info[1]
    


