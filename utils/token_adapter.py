import jwt
import datetime
from config.settings import Settings

settings = Settings()


class TokenAdapter:
    def __init__(self, token_expiration_minutes=1440):
        self.secret_key = settings.secret_key
        self.token_expiration_minutes = token_expiration_minutes

    async def create_token(self, user_id, full_name, email, profile):
        experiment_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=self.token_expiration_minutes)
        payload = {
            "user_id": user_id,
            "full_name": full_name,
            "email": email,
            "profile": profile,
            "exp": experiment_time
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    async def create_token_pronto(self, user_id, full_name, profile):
        experiment_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=self.token_expiration_minutes)
        payload = {
            "user_id": user_id,
            "full_name": full_name,
            "profile": profile,
            "exp": experiment_time
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')

    async def decode_token(self, token):
        return jwt.decode(token, self.secret_key, algorithms='HS256')
