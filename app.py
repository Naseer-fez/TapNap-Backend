from flask import Flask,request
from models.LoginSql import db
from models.LinksTable import Links #Just so the table is  created early
from utils.DB.CleaningDb import ClearingData
# from utils.extenstion import Serializer
from dotenv import load_dotenv
import os 
import threading
# from utils.DB.CleaningDb 
from routes.LinkPage.index import MainPg
from routes.LinkPage.Codepage import Codepg
from routes.LoginPage.Login import LoginBP
from routes.CreateAccount.CreaAcc import CreatBp
# from routes.Forgot.Email import FrgEmail
from flask_cors import CORS
from utils.Logger import logs
load_dotenv()

# def Backgrouncleaning():
#         cleaningdb=threading.Thread(target=ClearingData,daemon=True)
#         cleaningdb.start()
#         pass

def CreateApp():
    app=Flask(__name__)
    #Data Base 
    DatbaseUserName=os.getenv("DatbaseUserName")
    DatabasePassword=os.getenv("DatabasePassword")
    DatabaseHost=os.getenv("DatabaseHost")
    DatabaseName=os.getenv("DataBaseName")

    try:
        # app.config['SQLALCHEMY_DATABASE_URI']=os.getenv("SupaBase")
        # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DatbaseUserName}:{DatabasePassword}@{DatabaseHost}/{DatabaseName}"
        #  app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://root:{Database}@localhost/tapnap"
    except Exception as e:
        print(e)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' ##Trace back Database
    Key=os.getenv("SECRETKEY")
    app.secret_key=Key
    from itsdangerous import URLSafeSerializer
    Serializer=URLSafeSerializer(app.secret_key)
    db.init_app(app)

    #Bck cleaning 


    try:
        with app.app_context():
                db.create_all()
                # if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
                #     threading.Thread(target=ClearingData, daemon=True).start()

    except Exception as e:
        logs(e)
        print(e)
        
    #All Endpionts Regestering
    app.register_blueprint(LoginBP)
    app.register_blueprint(CreatBp)
    app.register_blueprint(MainPg)
    app.register_blueprint(Codepg)
    # app.register_blueprint(FrgEmail)
    # #Frontend
    FrontendURL=os.getenv("FrontendURL")
    Cors=CORS(app,resources={r"/*":{"origins":FrontendURL}})
    #Rate Limiter
    return app

app=CreateApp()




if __name__=="__main__":
    # app.run(debug=True,port=5000,host='0.0.0.0')
    # app.run(debug=True,port=5001)
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        cleaningdb=threading.Thread(target=ClearingData,args=(app,),daemon=True)
        cleaningdb.start()
        pass
    app.run(debug=True,port=500)

