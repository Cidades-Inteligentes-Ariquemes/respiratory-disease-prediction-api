from fastapi import HTTPException
from interfaces.create_user import CreateUser
from repository.user_repository import UserRepository
from utils.is_email_valid import is_email_valid
from utils.password_adapter import PasswordAdapter
from utils.token_adapter import TokenAdapter
import uuid


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.password_adapter = PasswordAdapter()
        self.token_adapter = TokenAdapter()

    async def create_user(self, user: CreateUser):
        print(f'Creating user in service: {user}')
        try:
            user = user.dict()

            for key, value in user.items():
                if not value:
                    raise HTTPException(status_code=400, detail={"message": f'Error adding user: {key} cannot be empty',
                                                                 "status_code": 400})
            
            if user['profile'] not in ['Administrador', 'Usuario_comum']:
                raise HTTPException(status_code=422, detail={"message": f'Error adding user: profile must be Administrador or Usuario_comum',
                                                             "status_code": 422})
            
            if not is_email_valid(user['email']):
                raise HTTPException(status_code=422, detail={"message": f'Error adding user: email is not valid',
                                                             "status_code": 422})
            

            user_exists = await self.user_repository.get_user_by_email(user['email'])


            if user_exists:
                raise HTTPException(status_code=422, detail={"message": f'Error adding user: email already exists',
                                                             "status_code": 422})
            
            user['password'] = await self.password_adapter.hash_password(user['password'])

            user_with_id = {
                "id": str(uuid.uuid4()),
                **user
            }
            
                        
            user_added = await self.user_repository.create_user(user_with_id)

            if user_added['added']:
                return {
                    "detail": {
                        "message": "User added successfully",
                        "user_id": user_added['id'],
                        "status_code": 201
                    }
                }
            else:
                raise HTTPException(status_code=500, detail={"message": "Error adding user",
                                                             "status_code": 500})
            
        except HTTPException as http_exc:
            raise http_exc
    

    async def login_user(self, user):
        print(f'Login user in service')
        try:
            user = user.dict()
            user_exists = await self.user_repository.get_user_by_email(user['email'])
            if user_exists:
                if await self.password_adapter.verify_password(user['password'], user_exists['password']):
                    token = await self.token_adapter.create_token(user_exists['id'], user_exists['full_name'], user_exists['email'], user_exists['profile'])
                    return {
                        "detail": {
                            "message": "User logged in successfully",
                            'user_id': str(user_exists['id']),
                            'user_full_name': str(user_exists['full_name']),
                            "token": token,
                            "status_code": 200
                        }
                    }
                else:
                    raise HTTPException(status_code=401, detail={"message": "Error logging in user: password is incorrect",
                                                                 "status_code": 401})
            else:
                raise HTTPException(status_code=404, detail={"message": "Error logging in user: user not found",
                                                             "status_code": 404})
        except HTTPException as http_exc:
            raise http_exc
        
    
    async def get_user_by_id(self, id: str):
        print(f'Get user by id in service')
        try:
            user = await self.user_repository.get_user_by_id(id)

            if user:
                user_without_password = {key: user[key] for key in user if key != 'password'}
                return {
                    "detail": {
                        "message": "User found",
                        "user": user_without_password,
                        "status_code": 200
                    }
                }
            else:
                raise HTTPException(status_code=404, detail={"message": "Error getting user by id: user not found",
                                                             "status_code": 404})
        except HTTPException as http_exc:
            raise http_exc
        
    
    async def get_users(self):
        print(f'Get users in service')
        try:
            users = await self.user_repository.get_users()
            if users:
                return {
                    "detail": {
                        "message": "Users found",
                        "users": users,
                        "status_code": 200
                    }
                }
            else:
                raise HTTPException(status_code=404, detail={"message": "Error getting users: users not found",
                                                             "status_code": 404})
        except HTTPException as http_exc:
            raise http_exc
        

    async def update_user(self, id: str, user):
        print(f'Update user in service')
        try:
            user = user.dict()
            for key, value in user.items():
                if not value:
                    raise HTTPException(status_code=400,
                                        detail={"message": f"Error updating user: {key} cannot be empty",
                                                "status_code": 400})
                
            user_exists = await self.user_repository.get_user_by_id(id)
                
            if user_exists:
                user['password'] = user_exists['password']
                print(f'User exists: {user_exists}')
                user_to_update = {
                    "id": id,
                    **user
                }
                user_updated = await self.user_repository.update_user(id, user_to_update)
                if user_updated['updated']:
                    return {
                        "detail": {
                            "message": "User updated successfully",
                            "user_id": id,
                            "status_code": 200
                        }
                    }
                else:
                    raise HTTPException(status_code=500, detail={"message": "Error updating user",
                                                                 "status_code": 500})
            else:
                raise HTTPException(status_code=404, detail={"message": "Error updating user: user not found",
                                                             "status_code": 404})
        except HTTPException as http_exc:
            raise http_exc
        
    

    async def update_password(self, user):
        print(f'Update password in service')
        try:
            user = user.dict()
            for key, value in user.items():
                if not value:
                    raise HTTPException(status_code=400,
                                        detail={"message": f"Error updating password: {key} cannot be empty",
                                                "status_code": 400})
            
            user_exists = await self.user_repository.get_user_by_email(user['email'])
            if user_exists:
                user['NewPassword'] = await self.password_adapter.hash_password(user['NewPassword'])
               
                user_updated = await self.user_repository.update_password_user(user_exists['id'], user['NewPassword'])
                if user_updated['updated']:
                    return {
                        "detail": {
                            "message": "Password updated successfully",
                            "user_email": user_exists['email'],
                            "status_code": 200
                        }
                    }
                else:
                    raise HTTPException(status_code=500, detail={"message": "Error updating password",
                                                                 "status_code": 500})
            else:
                raise HTTPException(status_code=404, detail={"message": "Error updating password: user not found",
                                                             "status_code": 404})
        except HTTPException as http_exc:
            raise http_exc
    

    async def delete_user(self, id: str):
        print(f'Delete user in service')
        try:
            user_exists = await self.user_repository.get_user_by_id(id)
            if user_exists:
                user_deleted = await self.user_repository.delete_user(id)
                if user_deleted['deleted']:
                    return {
                        "detail": {
                            "message": "User deleted successfully",
                            "user_id": id,
                            "status_code": 200
                        }
                    }
                else:
                    raise HTTPException(status_code=500, detail={"message": "Error deleting user",
                                                                 "status_code": 500})
            else:
                raise HTTPException(status_code=404, detail={"message": "Error deleting user: user not found",
                                                             "status_code": 404})
        except HTTPException as http_exc:
            raise http_exc