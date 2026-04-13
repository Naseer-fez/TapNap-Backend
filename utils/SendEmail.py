from dotenv import load_dotenv
import os
import smtplib as smpt
import ssl
from email.message import EmailMessage
from utils.Logger import logs
load_dotenv()

email=os.getenv("Email")
password=os.getenv("Email_password")





def Messages_to_send(to,content:str,subject:str,frm=email):
    receiver = f"{to}@gmail.com" if "@" not in to else to
    msg=EmailMessage()
    msg["Subject"]=subject
    msg["To"]=receiver
    msg["From"]=frm
    msg.set_content(content)
    return __email_sender(Message=msg)
    
        



                
                
def __email_sender(Message):
        cont=ssl.create_default_context()
        GMAIL_SERVER = "smtp.gmail.com"
        try:
            with smpt.SMTP_SSL(host=GMAIL_SERVER,port=465,context=cont) as server:
                server.login(email,password)
                server.send_message(Message)
                return 1
        except Exception as e:
            logs()
            return str(e)
    


    
