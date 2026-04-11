from flask import Blueprint,jsonify,request
from utils.APIRateLimiter import RequiredRateLimiter
from .TransferDB import Gateway
MainPg=Blueprint("MainPg",__name__)

@MainPg.route("/",methods=["POST"])
@RequiredRateLimiter()
def Mainpage():
    if request.method=="POST":
        Client=request.get_json(force=True)
        Data=dict()
        Data["Userid"]=Client.get("userid")
        Data["Code"]=Client.get("code")
        Data["Link"]=Client.get("link")
        Data["Password"]=Client.get("password")

        Info=Gateway(UserData=Data)
        # print(Info[0])
        return jsonify(Info[0]),Info[1]
            


