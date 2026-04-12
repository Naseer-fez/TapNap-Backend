from models.LinksTable import Links,db
import time
from utils.Logger import logs

def ClearingData(app):
        
        while True:
            with   app.app_context():
                
                try:
                    Crttime=int(time.time())
                    Todelete=Links.query.filter(Links.AllowedTime < Crttime).all()
                    for item in Todelete: 
                        db.session.delete(item)
                    db.session.commit()

                except TypeError as e:
                    db.session.rollback()
                    logs(e)
                    print(e)  
                    
                finally:
                    time.sleep(3600)