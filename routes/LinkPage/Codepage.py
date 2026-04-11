from flask import Blueprint,jsonify,request
from utils.APIRateLimiter import RequiredRateLimiter
from .RequestDB  import Getlink
Codepg=Blueprint("Codepg",__name__)


@Codepg.route("/Code/<int:Code>",methods=["GET"])
@Codepg.route("/Code/<int:Code>/<string:Password>")
@RequiredRateLimiter()
def CodePage(Code,Password=None):
    Data=Getlink(Code=Code,Password=Password)
    return jsonify(Data[0]),Data[1]







