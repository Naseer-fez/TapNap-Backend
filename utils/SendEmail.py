from dotenv import load_dotenv
import os
import resend
from utils.Logger import logs
load_dotenv()

email=os.getenv("Email")
resend.api_key = os.getenv("RESEND_API_KEY")




def Messages_to_send(to,content:str,subject:str,frm=email):
    receiver = f"{to}@gmail.com" if "@" not in to else to
    try:
        respond=resend.Email.send(
          {  "from":f"TapNap Assistant <onboarding@resend.dev>",
            "to":to,
            "subject":subject,
            "text":content})
        return 1
    except Exception as e:
        logs(str(e))
        return str(e)
    
        



                
                
# def Messages_to_send(to,content:str,subject:str,frm=email):
#     receiver = f"{to}@gmail.com" if "@" not in to else to
#     msg=EmailMessage()
#     msg["Subject"]=subject
#     msg["To"]=receiver
#     msg["From"]=frm
#     msg.set_content(content)
#     return __email_sender(Message=msg)
    
# def __email_sender(Message):
#         cont=ssl.create_default_context()
#         GMAIL_SERVER = "smtp.gmail.com"
#         try:
#             with smpt.SMTP_SSL(host=GMAIL_SERVER, port=465, context=cont, timeout=10) as server:
#                 server.login(email,password)
#                 server.send_message(Message)
#                 return 1
#         except Exception as e:
#             logs(e)
#             return str(e)
    


    
