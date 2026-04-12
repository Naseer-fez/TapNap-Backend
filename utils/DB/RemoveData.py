from models.LinksTable import Links,db
from utils.Logger import logs
from flask import current_app
def OldData(Data:dict):
        
            id=Data.ID
  
            try:

                Todelete=Links.query.filter_by(ID=id).first() 
                db.session.delete(Todelete)
                db.session.commit()
                
            except Exception as e:
                db.session.rollback()
                logs(e)
