from pydantic import BaseModel, EmailStr


class UserLoginPronto(BaseModel):
    username: str
    password: str