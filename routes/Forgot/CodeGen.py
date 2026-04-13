import secrets
import string
from utils.SendEmail import Messages_to_send


def OTP(email,length=4):
    Code=__digitcode()
    # (to,content:str,subject=None,frm=email)
    Subject="Your Verfication Code For Tap Nap"
    Content=f"""
    You Verfication Code to Log in Tap Nap is {Code}
    Dont Share your otp with anyone else.
    This code is only valid for  15 Mins only,After that u have to send the code again.
    
    """
    if Messages_to_send(to=email,subject=Subject,content=Content) !=1:
        return 'E'
    return Code
    


def __digitcode(length=4):
    characters = string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))
    


