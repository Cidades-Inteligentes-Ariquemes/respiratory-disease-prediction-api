from fastapi import HTTPException
from datetime import datetime
from interfaces.create_user import CreateUser
from repository.user_repository import UserRepository
from utils.is_email_valid import is_email_valid
from utils.password_adapter import PasswordAdapter
from utils.token_adapter import TokenAdapter
from random import randint
from config.settings import Settings
from utils.send_email import send_email
from datetime import timedelta
import uuid
from utils.logger import get_logger

logger = get_logger(__name__)

settings = Settings()

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
                raise HTTPException(status_code=403, detail={"message": f'Error adding user: email is not valid',
                                                             "status_code": 403})
            

            user_exists = await self.user_repository.get_user_by_email(user['email'])


            if user_exists:
                logger.error(f'Error adding user: email already exists')
                raise HTTPException(status_code=409, detail={"message": f'Error adding user: email already exists',
                                                             "status_code": 409})
            
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
                        raise HTTPException(status_code=400, detail={"message": "Error logging in user: token could not be created",
                                                                 "status_code": 400})
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
                    if len(user_witdout_id) > 0:
                        for user_saved in user_witdout_id:
                            if user['email'] == user_saved['email']:
                                logger.error(f'Error updating user: email already exists')
                                raise HTTPException(status_code=409, detail={"message": "Error updating user: email already exists",
                                                                    "status_code": 409})
                    
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
    

    async def send_verification_code(self, email: str):
        try:
            if not is_email_valid(email):
                logger.error(f"Error updating password: Invalid email")
                raise HTTPException(status_code=422, detail={"message": "Invalid email", "status_code": 422})
            user_exists = await self.user_repository.get_user_by_email(email)
            if not user_exists:
                logger.error(f"Error updating password: User not found")
                raise HTTPException(status_code=404, detail={"message": "User not found", "status_code": 404})
            
            verification_code = randint(100000, 999999)

            verification_email = await send_email(user_exists['full_name'], email, verification_code, settings.APP_NAME)

            if verification_email:
                logger.info(f"Verification code sent to email: {email}")

                user_data = {}

                user_data['id'] =  str(uuid.uuid4())
                user_data['user_id'] = user_exists['id']
                user_data['email'] = email
                user_data['code_verification'] = verification_code
                user_data['used'] = False
                user_data['created_at'] = str(datetime.now())
                user_data['expiration_at'] = datetime.now() + timedelta(minutes=10)

                saved_verification_code = await self.user_repository.add_code_verification(user_data)

                if saved_verification_code['added']:

                    logger.info(f"Verification code saved successfully")

                    return {
                        "detail": {
                            "message": "Verification code sent successfully",
                            "email": email,
                            "id_verification": user_data['id'],
                            "verification_code": verification_code,
                            "status_code": 200
                        }
                    }
            else:
                logger.error(f"Error sending verification code to email: {email}")
                raise HTTPException(status_code=500, detail={"message": "Error sending verification code to email", "status_code": 500})

        except HTTPException as http_exc:
            raise http_exc
    

    async def resend_verification_code(self, email: str, id_verification):
        try:

            if not is_email_valid(email):
                logger.error(f"Error updating password: Invalid email")
                raise HTTPException(status_code=422, detail={"message": "Invalid email", "status_code": 422})
            
            user_exists = await self.user_repository.get_user_by_email(email)

            if not user_exists:
                logger.error(f"Error updating password: User not found")
                raise HTTPException(status_code=404, detail={"message": "User not found", "status_code": 404})
            
            id_verification = id_verification.dict()
            id_verification = id_verification["id_verification"]

            code_exists = await self.user_repository.verify_code_exist(id_verification)
            # verifica se o código existe, se used é falso e se o código não expirou:
            if not code_exists:
                logger.info(f"Code not found")
                logger.info(f"Generating and seding new verification code")
                saved_verification_code = await self.send_verification_code(email)
                if saved_verification_code:
                    return {
                        "detail": {
                            "message": "New Verification code sent successfully",
                            "email": email,
                            "id_verification": saved_verification_code['detail']['id_verification'],
                            "verification_code": saved_verification_code['detail']['verification_code'],
                            "status_code": 200
                        }
                    }
                else:
                    logger.error(f"Error sending verification code to email: {email}")
                    raise HTTPException(status_code=500, detail={"message": "Error sending verification code to email", "status_code": 500})
            else:
                if code_exists['used'] or code_exists['expiration_at'] < datetime.now():
                    logger.info(f"Code expired or already used")
                    verification_code = randint(100000, 999999)
                    verification_email = await send_email(user_exists['full_name'], email, verification_code, settings.APP_NAME)
                else:
                    logger.info(f"Code not expired and not used. Resending the same code")
                    verification_code = code_exists['code_verification']
                    verification_email = await send_email(user_exists['full_name'], email, verification_code, settings.APP_NAME)

                if verification_email:
                    logger.info(f"Verification code sent to email: {email}")

                    code_exists['code_verification'] = verification_code
                    code_exists['expiration_at'] = datetime.now() + timedelta(minutes=10)

                    update_verification_code = await self.user_repository.update_code_verification_with_resend(code_exists, email, id_verification)

                    if update_verification_code['updated']:

                        logger.info(f"Verification code updated successfully")

                        return {
                            "detail": {
                                "message": "Existing verification code sent successfully",
                                "email": email,
                                "id_verification": update_verification_code['id_verification'],
                                "verification_code": verification_code,
                                "status_code": 200
                            }
                        }
                else:
                    logger.error(f"Error sending verification code to email: {email}")
                    raise HTTPException(status_code=500, detail={"message": "Error sending verification code to email", "status_code": 500})

        except HTTPException as http_exc:
            raise http_exc
    

    async def confirm_code_verification(self, email: str, code):
        try:

            if not is_email_valid(email):
                logger.error(f"Error verifying code: Invalid email")
                raise HTTPException(status_code=422, detail={"message": "Invalid email", "status_code": 422})
            
            user_exists = await self.user_repository.get_user_by_email(email)

            if not user_exists:
                logger.error(f"Error verifying code: User not found")
                raise HTTPException(status_code=404, detail={"message": "User not found", "status_code": 404})
            
            code_verification_wiht_id = await self.user_repository.get_code_verification(email, code)

            if not code_verification_wiht_id:
                logger.error(f"Error verifying code: Code not found")
                raise HTTPException(status_code=404, detail={"message": "Code not found", "status_code": 404})
        
            if code_verification_wiht_id['code_verification'] != code.code:
                logger.error(f"Error verifying code: Incorrect code")
                raise HTTPException(status_code=403, detail={"message": "Incorrect code", "status_code": 403})  
            
            if code_verification_wiht_id['expiration_at'] < datetime.now():
                logger.error(f"Error verifying code: Code expired")
                raise HTTPException(status_code=400, detail={"message": "Code expired", "status_code": 400})
            
            code_verification_wiht_id['used'] = True

            code_verification = await self.user_repository.update_code_verification(code_verification_wiht_id)

            if code_verification['updated']:
                logger.info(f"Code verification updated successfully")
                return {
                    "detail": {
                        "message": "Code verification with success",
                        "id_verification": code_verification_wiht_id["id"],
                        "user_id": user_exists["id"],
                        "user_email": email,
                        "status_code": 200
                    }
                }
            else:
                logger.error(f"Error verifying code: Code verification not updated")
                raise HTTPException(status_code=500, detail={"message": "Error verifying code", "status_code": 500})

        except HTTPException as http_exc:
            raise http_exc
    

    async def forgot_update_password(self, user_id: str, new_password):
        try:

            user_exists = await self.user_repository.get_user_by_id(user_id)

            if not user_exists:
                logger.error(f"Error updating password: User not found")
                raise HTTPException(status_code=404, detail={"message": "User not found", "status_code": 404})
            
            user_data = new_password.dict()
            code_exists = await self.user_repository.verify_code_exist(user_data["id_verification"])
            if not code_exists:
                logger.error(f"Error updating password: invalid code")
                raise HTTPException(status_code=403, detail={"message": "invalid code", "status_code": 403})
            
            if not code_exists['used']:
                logger.error(f"Error updating password: code not verified")
                raise HTTPException(status_code=400, detail={"message": "code not verified", "status_code": 400})
            
            user_data["new_password"] = await self.password_adapter.hash_password(user_data["new_password"])

            user = await self.user_repository.update_password_when_forgot_password(user_exists["email"], user_data["new_password"])

            if user["updated"]:
                return {
                    "detail": {
                        "message": "Password updated successfully",
                        "user_id": user_id,
                        "status_code": 200
                    }
                }
            else:
                logger.error(f"Error updating password: Password not updated")
                raise HTTPException(status_code=500, detail={"message": "Error updating password", "status_code": 500})

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
                
            feedback['prediction_made'] = feedback['prediction_made'].lower()
            feedback['feedback'] = feedback['feedback'].lower()
            feedback['correct_prediction'] = feedback['correct_prediction'].lower()

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

                for record in feedbacks:
                    disease = record['prediction_made']
                    feedback = record['feedback']

                    if disease not in contagem_feedback:
                        contagem_feedback[disease] = {
                            "total_quantity": 0,
                            "total_quantity_correct": 0
                        }
                    
                    contagem_feedback[disease]['total_quantity'] += 1

                    if feedback == 'sim':
                        contagem_feedback[disease]['total_quantity_correct'] += 1

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
                raise HTTPException(status_code=404, detail={"message": "There are no saved feedbacks",
                                                             "status_code": 404})
            else:
                logger.error(f'Error getting feedbacks: feedbacks not found')
                raise HTTPException(status_code=500, detail={"message": "Error getting feedbacks: feedbacks not found",
                                                             "status_code": 500})
        except HTTPException as http_exc:
            raise http_exc