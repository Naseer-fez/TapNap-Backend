from flask import Blueprint,jsonify,request
from utils.APIRateLimiter import RequiredRateLimiter
LoginBP=Blueprint("Login",__name__)

@LoginBP.route("/",methods=["POST"])
@RequiredRateLimiter()
def LoginPage():
    return "HII,hello"
    


