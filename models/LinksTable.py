from models.LoginSql import db
# from LoginSql import db
import time

class Links(db.Model):
    __tablename__="Links"
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)    
    UserId=db.Column(db.Integer, db.ForeignKey('User.id',ondelete='SET NULL'),index=True, nullable=True,default=None)
    Link=db.Column(db.String(768),unique=False,nullable=False)
    Password=db.Column(db.String(256),nullable=True)
    Code=db.Column(db.Integer,unique=True,nullable=False)
    CreatedTime= db.Column(db.BigInteger, default=lambda: int(time.time()),nullable=False)
    AllowedTime=db.Column(db.BigInteger, default=lambda: int(time.time())+864001,nullable=False)
    