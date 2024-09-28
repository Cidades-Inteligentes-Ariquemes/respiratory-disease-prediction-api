from fastapi import Request
from interfaces.create_user import CreateUser
from interfaces.user_login import UserLogin
from services.user_service import UserService
from interfaces.update_user import UpdateUser
from interfaces.update_password_user import UpdatePassword
from interfaces.create_feedback_user import CreateFeedbackUser
from interfaces.update_password_user_common import UpdatePasswordUserCommon
from interfaces.forgot_update_password_model import ForgotUpadatePassword
from interfaces.code_verification_model import CodeVerification
from interfaces.id_verification_model import IdVerification  
from utils import credentials_middleware


class UserController:
    def __init__(self):
        self.user_service = UserService()
        self.credentials_middleware = credentials_middleware.CredentialsMiddleware()

    async def create_user(self, request: Request, user: CreateUser):
        await self.credentials_middleware.verify_credentials(request)
        return await self.user_service.create_user(user)
    
    async def login_user(self, request: Request, user: UserLogin):
        await self.credentials_middleware.verify_credentials(request)
        return await self.user_service.login_user(user)
    
    async def get_user_by_id(self, request: Request, id: str):
        await self.credentials_middleware.verify_credentials(request)
        return await self.user_service.get_user_by_id(id)
    
    async def get_users(self, request: Request):
        await self.credentials_middleware.verify_credentials(request)
        return await self.user_service.get_users()
    
    async def update_user(self, request: Request, id: str, user: UpdateUser):
        await self.credentials_middleware.verify_credentials(request)
        return await self.user_service.update_user(id, user)
    
    async def update_password(self, request: Request, user: UpdatePassword):
        await self.credentials_middleware.verify_credentials(request)
        return await self.user_service.update_password(user)
    
    async def update_password_user_common(self, request: Request, id: str, user: UpdatePasswordUserCommon):
        await self.credentials_middleware.verify_credentials(request)
        return await self.user_service.update_password_user_common(id, user)
    
    async def send_verification_code(self, request: Request, email: str):
        await self.credentials_middleware.verify_credentials(request)
        return await self.user_service.send_verification_code(email)
    
    async def resend_verification_code(self, request: Request, email: str, id_verification: IdVerification):
        await self.credentials_middleware.verify_credentials(request)
        return await self.user_service.resend_verification_code(email, id_verification)
    
    async def confirm_code_verification(self, request: Request, email: str, code_verification: CodeVerification):
        await self.credentials_middleware.verify_credentials(request)
        return await self.user_service.confirm_code_verification(email, code_verification)
    
    async def forgot_update_password(self, request: Request, user_id: str, new_password: ForgotUpadatePassword):
        await self.credentials_middleware.verify_credentials(request)
        return await self.user_service.forgot_update_password(user_id, new_password)
    
    async def delete_user(self, request: Request, id: str):
        await self.credentials_middleware.verify_credentials(request)
        return await self.user_service.delete_user(id)
    
    async def create_feedback(self, request: Request, feedback: CreateFeedbackUser):
        await self.credentials_middleware.verify_credentials(request)
        return await self.user_service.create_feedback(feedback)
    
    async def get_feedback(self, request: Request):
        await self.credentials_middleware.verify_credentials(request)
        return await self.user_service.get_feedback()
