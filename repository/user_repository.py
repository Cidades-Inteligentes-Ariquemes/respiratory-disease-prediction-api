from typing import List, Dict
import psycopg2
from infra.database import get_database
from utils.logger import get_logger

logger = get_logger(__name__)


class UserRepository:

    def __init__(self):
        self.db_connection = get_database()
    
    async def create_user(self, user: Dict):
        try:
            with psycopg2.connect(self.db_connection) as connection:
                with connection.cursor() as cursor:
                    sql = """
                    INSERT INTO user_rx (id, full_name, email, profile, password)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                    """
                    values = (
                        user['id'],
                        user['full_name'],
                        user['email'],
                        user['profile'],
                        user['password']
                    )
                    cursor.execute(sql, values)
                    return_id = cursor.fetchone()[0]
                    connection.commit()
                    
                    return {
                        "id": return_id,
                        "email": user['email'],
                        "added": True
                    }
        except Exception as e:
            logger.error(f'Error creating user: {e}')
            return {
                "id": '',
                "added": False
            }
    
    async def get_user_by_email(self, email: str) -> Dict:
            
            try:
                connection = psycopg2.connect(self.db_connection)
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM user_rx WHERE email = %s", (email,))
                user = cursor.fetchone()
                cursor.close()
                connection.close()
    
                if user:
                    return {
                        "id": user[0],
                        "full_name": user[1],
                        "email": user[2],
                        "profile": user[3],
                        "password": user[4]
                    }
                else:
                    return None
            
            except Exception as e:
                logger.error(f'Error getting user by email: {e}')
                return None
    

    async def get_user_by_id(self, id: str) -> Dict:
        try:
            connection = psycopg2.connect(self.db_connection)
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM user_rx WHERE id = %s", (id,))
            user = cursor.fetchone()
            cursor.close()
            connection.close()

            if user:
                return {
                    "id": user[0],
                    "full_name": user[1],
                    "email": user[2],
                    "profile": user[3],
                    "password": user[4]
                }
            else:
                return None
        
        except Exception as e:
            logger.error(f'Error getting user by id: {e}')
            return None
        
    
    async def get_users(self) -> List[Dict]:
        try:
            connection = psycopg2.connect(self.db_connection)
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM user_rx")
            users = cursor.fetchall()
            cursor.close()
            connection.close()

            if users:
                return [
                    {
                        "id": user[0],
                        "full_name": user[1],
                        "email": user[2],
                        "profile": user[3],
                    } for user in users
                ]
            else:
                return []
        
        except Exception as e:
            logger.error(f'Error getting users: {e}')
            return []
    

    async def update_user(self, id: str, user: Dict):
        try:
            with psycopg2.connect(self.db_connection) as connection:
                with connection.cursor() as cursor:
                    sql = """
                    UPDATE user_rx
                    SET full_name = %s, email = %s, profile = %s
                    WHERE id = %s
                    """
                    values = (
                        user['full_name'],
                        user['email'],
                        user['profile'],
                        id
                    )
                    cursor.execute(sql, values)
                    connection.commit()
                    
                    return {
                        "id": id,
                        "email": user['email'],
                        "updated": True
                    }
        except Exception as e:
            logger.error(f'Error updating user: {e}')
            return {
                "id": '',
                "updated": False
            }
    

    async def update_password_user(self, id: str, password: str):
        try:
            with psycopg2.connect(self.db_connection) as connection:
                with connection.cursor() as cursor:
                    sql = """
                    UPDATE user_rx
                    SET password = %s
                    WHERE id = %s
                    """
                    values = (
                        password,
                        id
                    )
                    cursor.execute(sql, values)
                    connection.commit()
                    
                    return {
                        "id": id,
                        "updated": True
                    }
        except Exception as e:
            logger.error(f'Error updating password: {e}')
            return {
                "id": '',
                "updated": False
            }
        
    async def add_code_verification(self, user_data: Dict) -> Dict:
        try:
            connection = psycopg2.connect(self.db_connection)
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO forgot_password (id, user_id, user_email, code_verification, used, created_at, expiration_at) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id",
                (user_data["id"], user_data["user_id"], user_data["email"], user_data["code_verification"], user_data["used"], user_data["created_at"], user_data["expiration_at"])
            )
            logged_id = cursor.fetchone()[0]
            connection.commit()
            cursor.close()
            connection.close()
            logger.info(f"Code verification added for {user_data['email']}")
            return {
                "logged_id": logged_id,
                "added": True
            }
        except Exception as e:
            logger.error(f"Error adding log: {e}")
            return {
                "logged_id": "",
                "added": False
            }
    
    async def get_code_verification(self, email: str, code: int) -> Dict:
        try:
            connection = psycopg2.connect(self.db_connection)
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM forgot_password WHERE user_email = %s AND code_verification = %s AND used = %s", (email, code.code, False))
            code_saved = cursor.fetchone()
            cursor.close()
            connection.close()
            if code_saved:
                logger.info(f"Code verification found for {email}")
                return {
                    "id": code_saved[0],
                    "user_id": code_saved[1],
                    "email": code_saved[2],
                    "code_verification": code_saved[3],
                    "used": code_saved[4],
                    "created_at": code_saved[5],
                    "expiration_at": code_saved[6]
                }
            else:
                logger.info(f"Code verification not found")
                return None
        except Exception as e:
            logger.error(f"Error fetching code verification: {e}")
            return None
    
    async def verify_code_exist(self, id: str) -> Dict:
        try:
            connection = psycopg2.connect(self.db_connection)
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM forgot_password WHERE id = %s", (id,))
            code_saved = cursor.fetchone()
            cursor.close()
            connection.close()
            if code_saved:
                logger.info(f"Code verification found for {id}")
                return {
                    "id": code_saved[0],
                    "user_id": code_saved[1],
                    "email": code_saved[2],
                    "code_verification": code_saved[3],
                    "used": code_saved[4],
                    "created_at": code_saved[5],
                    "expiration_at": code_saved[6]
                }
            else:
                logger.info(f"Code verification not found")
                return None
        except Exception as e:
            logger.error(f"Error fetching code verification: {e}")
            return None
    
    async def update_code_verification(self, code_verification: Dict) -> Dict:
        try:
            connection = psycopg2.connect(self.db_connection)
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE forgot_password SET used = %s WHERE user_email = %s AND code_verification = %s RETURNING id",
                (True, code_verification['email'], code_verification['code_verification'])
            )
            updated_id = cursor.fetchone()
            connection.commit()
            cursor.close()
            connection.close()
            if updated_id:
                logger.info(f"Code verification updated for {code_verification['email']}")
                return {
                    "email": code_verification['email'],
                    "updated": True,
                }
            else:
                logger.info(f"Code verification not found")
                return {
                    "email": "",
                    "updated": False,
                }
        except Exception as e:
            logger.error(f"Error updating code verification: {e}")
            return {
                "email": "",
                "updated": False,
            }
    
    async def update_code_verification_with_resend(self, code_data: Dict, email, id_verification) -> Dict:
        try:
            connection = psycopg2.connect(self.db_connection)
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE forgot_password SET used = %s, code_verification = %s, expiration_at = %s WHERE user_email = %s AND id = %s RETURNING id",
                (False, code_data['code_verification'], code_data['expiration_at'], email, id_verification)
            )

            updated_id = cursor.fetchone()
            connection.commit()
            cursor.close()
            connection.close()
            if updated_id:
                logger.info(f"Code verification updated for {code_data['email']}")
                return {
                    "id_verification": updated_id[0],
                    "email": code_data['email'],
                    "updated": True,
                }
            else:
                logger.info(f"Code verification not found")
                return {
                    "email": "",
                    "updated": False,
                }
        except Exception as e:
            logger.error(f"Error updating code verification: {e}")
            return {
                "email": "",
                "updated": False,
            }
        
    async def update_password_when_forgot_password(self, email: str, password: str) -> Dict:
        try:
            connection = psycopg2.connect(self.db_connection)
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE user_rx SET password = %s WHERE email = %s RETURNING email",
                (password, email)
            )
            updated_email = cursor.fetchone()
            connection.commit()
            cursor.close()
            connection.close()
            if updated_email:
                logger.info(f"Password updated for {email}")
                return {
                    "email": email,
                    "updated": True,
                }
            else:
                logger.info(f"User {email} not found")
                return {
                    "email": "",
                    "updated": False,
                }
        except Exception as e:
            logger.error(f"Error updating password: {e}")
            return {
                "email": "",
                "updated": False,
            }
    
    async def delete_user(self, id: str):
        try:
            with psycopg2.connect(self.db_connection) as connection:
                with connection.cursor() as cursor:
                    sql = """
                    DELETE FROM user_rx
                    WHERE id = %s
                    """
                    cursor.execute(sql, (id,))
                    connection.commit()
                    
                    return {
                        "id": id,
                        "deleted": True
                    }
        except Exception as e:
            logger.error(f'Error deleting user: {e}')
            return {
                "id": '',
                "deleted": False
            }
    

    async def create_feedback(self, feedback: Dict):
        try:
            with psycopg2.connect(self.db_connection) as connection:
                with connection.cursor() as cursor:
                    sql = """
                    INSERT INTO feedbacks (id, user_name, feedback, prediction_made, correct_prediction, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """
                    values = (
                        feedback['id'],
                        feedback['user_name'],
                        feedback['feedback'],
                        feedback['prediction_made'],
                        feedback['correct_prediction'],
                        feedback['created_at']
                    )
                    cursor.execute(sql, values)
                    return_id = cursor.fetchone()[0]
                    connection.commit()
                    
                    return {
                        "id": return_id,
                        "added": True
                    }
        except Exception as e:
            logger.error(f'Error creating feedback: {e}')
            return {
                "id": '',
                "added": False
            }
    

    async def get_feedback(self) -> List[Dict]:
        try:
            connection = psycopg2.connect(self.db_connection)
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM feedbacks")
            feedbacks = cursor.fetchall()
            cursor.close()
            connection.close()

            if feedbacks:
                return [
                    {
                        "feedback": feedback[2],
                        "prediction_made": feedback[3],
                        "correct_prediction": feedback[4],
                    } for feedback in feedbacks
                ]
            else:
                return []
        
        except Exception as e:
            logger.error(f'Error getting feedbacks: {e}')
            return []

    
