from fastapi import Request
from interfaces.create_user import CreateUser
from interfaces.user_login import UserLogin
from services.user_service import UserService
from interfaces.update_user import UpdateUser
from interfaces.update_password_user import UpdatePassword


class UserController:
    def __init__(self):
        self.user_service = UserService()

    async def create_user(self, request: Request, user: CreateUser):
        print(f'Creating user in controller: {user}')
        return await self.user_service.create_user(user)
    
    async def login_user(self, request: Request, user: UserLogin):
        print(f'Login user in controller')
        return await self.user_service.login_user(user)
    
    async def get_user_by_id(self, request: Request, id: str):
        print(f'Get user by id in controller')
        return await self.user_service.get_user_by_id(id)
    
    async def get_users(self, request: Request):
        print(f'Get users in controller')
        return await self.user_service.get_users()
    
    async def update_user(self, request: Request, id: str, user: UpdateUser):
        print(f'Update user in controller')
        return await self.user_service.update_user(id, user)
    
    async def update_password(self, request: Request, user: UpdatePassword):
        print(f'Update password in controller')
        return await self.user_service.update_password(user)
    
    async def delete_user(self, request: Request, id: str):
        print(f'Delete user in controller')
        return await self.user_service.delete_user(id)
