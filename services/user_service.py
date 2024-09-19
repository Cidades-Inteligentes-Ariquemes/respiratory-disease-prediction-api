from fastapi import HTTPException
from datetime import datetime
from interfaces.create_user import CreateUser
from repository.user_repository import UserRepository
from utils.is_email_valid import is_email_valid
from utils.password_adapter import PasswordAdapter
from utils.token_adapter import TokenAdapter
import uuid
from utils.logger import get_logger

logger = get_logger(__name__)


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.password_adapter = PasswordAdapter()
        self.token_adapter = TokenAdapter()

    async def create_user(self, user: CreateUser):
        try:
            user = user.dict()

            for key, value in user.items():
                if not value:
                    logger.error(f'Error adding user: {key} cannot be empty')
                    raise HTTPException(status_code=400, detail={"message": f'Error adding user: {key} cannot be empty',
                                                                 "status_code": 400})
            
            if user['profile'] not in ['Administrador', 'Usuario_comum']:
                logger.error(f'Error adding user: profile must be Administrador or Usuario_comum')
                raise HTTPException(status_code=422, detail={"message": f'Error adding user: profile must be Administrador or Usuario_comum',
                                                             "status_code": 422})
            
            if not is_email_valid(user['email']):
                logger.error(f'Error adding user: email is not valid')
                raise HTTPException(status_code=422, detail={"message": f'Error adding user: email is not valid',
                                                             "status_code": 422})
            

            user_exists = await self.user_repository.get_user_by_email(user['email'])


            if user_exists:
                logger.error(f'Error adding user: email already exists')
                raise HTTPException(status_code=422, detail={"message": f'Error adding user: email already exists',
                                                             "status_code": 422})
            
            user['password'] = await self.password_adapter.hash_password(user['password'])

            user_with_id = {
                "id": str(uuid.uuid4()),
                **user
            }
            
                        
            user_added = await self.user_repository.create_user(user_with_id)

            if user_added['added']:
                logger.info(f'User added successfully')
                return {
                    "detail": {
                        "message": "User added successfully",
                        "user_id": user_added['id'],
                        "status_code": 201
                    }
                }
            else:
                logger.error(f'Error adding user')
                raise HTTPException(status_code=500, detail={"message": "Error adding user",
                                                             "status_code": 500})
            
        except HTTPException as http_exc:
            raise http_exc
    

    async def login_user(self, user):
        try:
            user = user.dict()
            user_exists = await self.user_repository.get_user_by_email(user['email'])
            if user_exists:
                logger.info(f"User exists: {user_exists['id']}")
                if await self.password_adapter.verify_password(user['password'], user_exists['password']):
                    token = await self.token_adapter.create_token(user_exists['id'], user_exists['full_name'], user_exists['email'], user_exists['profile'])
                    if not token:
                        logger.error(f'Error logging in user: token could not be created')
                        raise HTTPException(status_code=500, detail={"message": "Error logging in user: token could not be created",
                                                                 "status_code": 500})
                    logger.info(f'User logged in successfully')
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
                    logger.error(f'Error logging in user: password is incorrect')
                    raise HTTPException(status_code=401, detail={"message": "Error logging in user: password is incorrect",
                                                                 "status_code": 401})
            else:
                logger.error(f'Error logging in user: user not found')
                raise HTTPException(status_code=404, detail={"message": "Error logging in user: user not found",
                                                             "status_code": 404})
        except HTTPException as http_exc:
            raise http_exc
        
    
    async def get_user_by_id(self, id: str):
        try:
            user = await self.user_repository.get_user_by_id(id)

            if user:
                logger.info(f"User found successfully: {user['id']}") 
                user_without_password = {key: user[key] for key in user if key != 'password'}
                return {
                    "detail": {
                        "message": "User found",
                        "user": user_without_password,
                        "status_code": 200
                    }
                }
            else:
                logger.error(f'Error getting user by id: user not found')
                raise HTTPException(status_code=404, detail={"message": "Error getting user by id: user not found",
                                                             "status_code": 404})
        except HTTPException as http_exc:
            raise http_exc
        
    
    async def get_users(self):
        try:
            users = await self.user_repository.get_users()
            if users:
                logger.info(f'Users found successfully')
                return {
                    "detail": {
                        "message": "Users found",
                        "users": users,
                        "status_code": 200
                    }
                }
            else:
                logger.error(f'Error getting users: users not found')
                raise HTTPException(status_code=404, detail={"message": "Error getting users: users not found",
                                                             "status_code": 404})
        except HTTPException as http_exc:
            raise http_exc
        

    async def update_user(self, id: str, user):
        try:
            user = user.dict()
            for key, value in user.items():
                if not value:
                    logger.error(f'Error updating user: {key} cannot be empty')
                    raise HTTPException(status_code=400,
                                        detail={"message": f"Error updating user: {key} cannot be empty",
                                                "status_code": 400})
                
            user_exists = await self.user_repository.get_user_by_id(id)
            
            if user_exists:
                users = await self.user_repository.get_users()
                if users:
                    user_witdout_id = [user for user in users if user['id'] != id]
                    print(f'len user_witdout_id: {len(user_witdout_id)}')
                    if len(user_witdout_id) > 0:
                        for user_saved in user_witdout_id:
                            if user['email'] == user_saved['email']:
                                print('Entrei aqui')
                                logger.error(f'Error updating user: email already exists')
                                raise HTTPException(status_code=422, detail={"message": "Error updating user: email already exists",
                                                                    "status_code": 422})
                    
                    print('Entrei aqui 2')
                    logger.info(f'User exists: {id}')
                    user['password'] = user_exists['password']
                    user_to_update = {
                        "id": id,
                        **user
                    }
                    user_updated = await self.user_repository.update_user(id, user_to_update)
                    if user_updated['updated']:
                        logger.info(f'User with id: {id} updated successfully')
                        return {
                            "detail": {
                                "message": "User updated successfully",
                                "user_id": id,
                                "status_code": 200
                            }
                        }
                    else:
                        logger.error(f'Error updating user')
                        raise HTTPException(status_code=500, detail={"message": "Error updating user",
                                                                        "status_code": 500})
                else:
                    logger.error(f'Error updating user: users not found')
                    raise HTTPException(status_code=404, detail={"message": "Error updating user: users not found",
                                                             "status_code": 404})
            else:
                logger.error(f'Error updating user: user not found')
                raise HTTPException(status_code=404, detail={"message": "Error updating user: user not found",
                                                             "status_code": 404})
        except HTTPException as http_exc:
            raise http_exc
        
    

    async def update_password(self, user):
        try:
            user = user.dict()
            for key, value in user.items():
                if not value:
                    logger.error(f'Error updating password: {key} cannot be empty')
                    raise HTTPException(status_code=400,
                                        detail={"message": f"Error updating password: {key} cannot be empty",
                                                "status_code": 400})
            
            user_exists = await self.user_repository.get_user_by_email(user['email'])
            if user_exists:
                logger.info(f"User exists: {user_exists['id']}")
                user['NewPassword'] = await self.password_adapter.hash_password(user['NewPassword'])
               
                user_updated = await self.user_repository.update_password_user(user_exists['id'], user['NewPassword'])
                if user_updated['updated']:
                    logger.info(f"Password updated user with id: {user_exists['id']} successfully")
                    return {
                        "detail": {
                            "message": "Password updated successfully",
                            "user_email": user_exists['email'],
                            "status_code": 200
                        }
                    }
                else:
                    logger.error(f'Error updating password')
                    raise HTTPException(status_code=500, detail={"message": "Error updating password",
                                                                 "status_code": 500})
            else:
                logger.error(f'Error updating password: user not found')
                raise HTTPException(status_code=404, detail={"message": "Error updating password: user not found",
                                                             "status_code": 404})
        except HTTPException as http_exc:
            raise http_exc
    

    async def update_password_user_common(self, id: str, user):
        try:
            user = user.dict()
            for key, value in user.items():
                if not value:
                    logger.error(f'Error updating password: {key} cannot be empty')
                    raise HTTPException(status_code=400,
                                        detail={"message": f"Error updating password: {key} cannot be empty",
                                                "status_code": 400})
            
            user_exists = await self.user_repository.get_user_by_id(id)
            if user_exists:
                logger.info(f"User exists: {user_exists['id']}")
                
                # comparar a senha atual com a senha que o usuário informou
                if not await self.password_adapter.verify_password(user['CurrentPassword'], user_exists['password']):
                    logger.error(f'Error updating password: old password is incorrect')
                    raise HTTPException(status_code=401, detail={"message": "Error updating password: current password is incorrect",
                                                                 "status_code": 401})

                user['NewPassword'] = await self.password_adapter.hash_password(user['NewPassword'])

                user_updated = await self.user_repository.update_password_user(id, user['NewPassword'])

                if user_updated['updated']:
                    logger.info(f"Password updated user with id: {user_exists['id']} successfully")
                    return {
                        "detail": {
                            "message": "Password updated successfully",
                            "user_id": user_exists['id'],
                            "status_code": 200
                        }
                    }
                else:
                    logger.error(f'Error updating password')
                    raise HTTPException(status_code=500, detail={"message": "Error updating password",
                                                                 "status_code": 500})
            else:
                logger.error(f'Error updating password: user not found')
                raise HTTPException(status_code=404, detail={"message": "Error updating password: user not found",
                                                             "status_code": 404})
        except HTTPException as http_exc:
            raise http_exc
    

    async def delete_user(self, id: str):
        try:
            user_exists = await self.user_repository.get_user_by_id(id)
            if user_exists:
                logger.info(f'User exists: {id}')
                user_deleted = await self.user_repository.delete_user(id)
                if user_deleted['deleted']:
                    logger.info(f'User with id: {id} deleted successfully')
                    return {
                        "detail": {
                            "message": "User deleted successfully",
                            "user_id": id,
                            "status_code": 200
                        }
                    }
                else:
                    logger.error(f'Error deleting user')
                    raise HTTPException(status_code=500, detail={"message": "Error deleting user",
                                                                 "status_code": 500})
            else:
                logger.error(f'Error deleting user: user not found')
                raise HTTPException(status_code=404, detail={"message": "Error deleting user: user not found",
                                                             "status_code": 404})
        except HTTPException as http_exc:
            raise http_exc
    

    async def create_feedback(self, feedback):
        try:
            feedback = feedback.dict()
            for key, value in feedback.items():
                if not value:
                    logger.error(f'Error adding feedback: {key} cannot be empty')
                    raise HTTPException(status_code=400, detail={"message": f'Error adding feedback: {key} cannot be empty',
                                                                 "status_code": 400})
            
            feedback_with_id = {
                "id": str(uuid.uuid4()),
                **feedback,
                'created_at': str(datetime.now())
            }
            
            feedback_added = await self.user_repository.create_feedback(feedback_with_id)
            if feedback_added['added']:
                logger.info(f'Feedback added successfully')
                return {
                    "detail": {
                        "message": "Feedback added successfully",
                        "feedback_id": feedback_added['id'],
                        "status_code": 201
                    }
                }
            else:
                logger.error(f'Error adding feedback')
                raise HTTPException(status_code=500, detail={"message": "Error adding feedback",
                                                             "status_code": 500})
        except HTTPException as http_exc:
            raise http_exc
    

    async def get_feedback(self):
        try:
            feedbacks = await self.user_repository.get_feedback()
            if feedbacks and len(feedbacks) > 0:

                contagem_feedback = {}

                for item in feedbacks:
                    feedback = item['feedback']
                    if feedback in contagem_feedback:
                        contagem_feedback[feedback] += 1
                    else:
                        contagem_feedback[feedback] = 1

                logger.info(f'Feedbacks found successfully')

                return {
                    "detail": {
                        "message": "Feedbacks found",
                        "feedbacks": contagem_feedback,
                        "status_code": 200
                    }
                }
            elif len(feedbacks) == 0:
                logger.error(f'Error getting feedbacks: feedbacks not found')
                raise HTTPException(status_code=200, detail={"message": "There are no saved feedbacks",
                                                             "status_code": 200})
            else:
                logger.error(f'Error getting feedbacks: feedbacks not found')
                raise HTTPException(status_code=404, detail={"message": "Error getting feedbacks: feedbacks not found",
                                                             "status_code": 404})
        except HTTPException as http_exc:
            raise http_exc