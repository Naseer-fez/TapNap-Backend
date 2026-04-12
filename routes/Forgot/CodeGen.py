import secrets
import string



def OTP(length=4):
    characters = string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))
    


