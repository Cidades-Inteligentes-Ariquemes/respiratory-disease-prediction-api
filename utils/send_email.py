import smtplib
import email.message
from config.settings import Settings
import requests as req

settings = Settings()


async def send_email(user, email_user, code_verification, app_name):

    try:
        result = req.post('https://simple-mail-compose-simple-mail.o3luz9.easypanel.host/send-email', json={
            "from": settings.EMAIL,
            "to": email_user,
            "subject": f"Recuperação de senha {app_name}",
            "context": {
                "user": user,
                "code_verification": code_verification
            },
            "template": "main"
        })
        return True
    except Exception as e:
        print("Error: ", e)
        return False