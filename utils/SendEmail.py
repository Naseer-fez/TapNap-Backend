import os
import requests
from utils.Logger import logs
def Messages_to_send(to: str, content: str, subject: str):
    receiver = f"{to}@gmail.com" if "@" not in to else to
    
    api_key = os.getenv("EmailAPi",)
    sender_email = os.getenv("SendEmail")
    sender_name = os.getenv("SendEmail", "TapNap Assistant")

    if not api_key or not sender_email:
        return "Error: Email configuration missing in environment"

    url = "https://api.brevo.com/v3/smtp/email"
    
    payload = {
        "sender": {"name": sender_name, "email": sender_email},
        "to": [{"email": receiver}],
        "replyTo": {"name": sender_name, "email": sender_email},
        "subject": subject,
        "textContent": content
    }
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": api_key
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        
        if response.status_code in [200, 201, 202]:
            return 1
        return f"Error {response.status_code}: {response.text}"
            
    except requests.exceptions.RequestException as e:
        logs(str(e))
        return str(e)