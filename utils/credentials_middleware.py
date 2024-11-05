from fastapi import Request, HTTPException
import jwt
from config.settings import Settings
from utils import list_routes_user_common

settings = Settings()

class CredentialsMiddleware:

    @staticmethod
    async def verify_credentials(request: Request):
        list_routes = list_routes_user_common.list_routes_user_common()
        api_key = request.headers.get('api_key')
        token_value = request.headers.get('Authorization')
        allowed_paths = [
            '/login',
            '/login-pronto',
            '/send-verification-code/',
            '/confirm-code-verification/',
            '/forgot/update-password/',
            '/resend-verification-code/'
        ]
        if any([request.url.path.startswith(path) for path in allowed_paths]):
            CredentialsMiddleware.verify_api_key(api_key)
        elif request.url.path in list_routes:
            CredentialsMiddleware.verify_api_key(api_key)
            CredentialsMiddleware.verify_token(token_value)
        else:
            CredentialsMiddleware.verify_api_key(api_key)
            CredentialsMiddleware.verify_token(token_value)
            CredentialsMiddleware.can_access_admin(token_value)


    @staticmethod
    def verify_api_key(api_key: str):
        if not api_key:
            raise HTTPException(status_code=400, detail={"message": "API Key is required", "status_code": 400})
        if api_key != settings.api_key:
            raise HTTPException(status_code=403, detail={"message": "Invalid API Key", "status_code": 403})
    

    @staticmethod
    def verify_token(token_value: str):
        if token_value:
            token = token_value.split(' ')[1]
            try:
                jwt.decode(token, settings.secret_key, algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                raise HTTPException(status_code=403, detail={"message": "Token expired", "status_code": 403})
            except jwt.InvalidTokenError:
                raise HTTPException(status_code=403, detail={"message": "Invalid token", "status_code": 403})
        else:
            raise HTTPException(status_code=400, detail={"message": "Token is required", "status_code": 400})
        
    
    @staticmethod
    def can_access_admin(token_value: str):
        token = token_value.split(' ')[1]
        decoded_token = jwt.decode(token, settings.secret_key, algorithms=['HS256'])
        if decoded_token['profile'] != 'Administrador':
            raise HTTPException(status_code=403, detail={"message": "Unauthorized. This request can only be made by administrators.", "status_code": 403})
       
        