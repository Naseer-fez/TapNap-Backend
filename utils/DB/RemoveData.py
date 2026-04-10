from models.LinksTable import Links,db
from utils.Logger import logs
def OldData(Data:dict):
        from app import app
        id=Data.ID
        with   app.app_context():
            try:

                Todelete=Links.query.filter_by(ID=id).first() 
                db.session.delete(Todelete)
                db.session.commit()
                
            except Exception as e:
                db.session.rollback()
                logs(e)
                print(e)