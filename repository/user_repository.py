from typing import List, Dict
import psycopg2
from infra.database import get_database


class UserRepository:

    def __init__(self):
        self.db_connection = get_database()
    
    async def create_user(self, user: Dict):
        print(f'Creating user in repository: {user}')
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
            print(f'Error: {e}')
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
                print(f'Error: {e}')
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
            print(f'Error: {e}')
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
            print(f'Error: {e}')
            return []
    

    async def update_user(self, id: str, user: Dict):
        print(f'Updating user in repository: {user}')
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
            print(f'Error: {e}')
            return {
                "id": '',
                "updated": False
            }
    

    async def update_password_user(self, id: str, password: str):
        print(f'Updating password in repository')
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
            print(f'Error: {e}')
            return {
                "id": '',
                "updated": False
            }
    
    async def delete_user(self, id: str):
        print(f'Deleting user in repository')
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
            print(f'Error: {e}')
            return {
                "id": '',
                "deleted": False
            }

    
