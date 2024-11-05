from pydantic import BaseModel, EmailStr


class UpdatePassword(BaseModel):
    email: EmailStr
    NewPassword: str