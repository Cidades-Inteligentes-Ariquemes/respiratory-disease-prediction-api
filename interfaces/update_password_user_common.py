from pydantic import BaseModel, EmailStr


class UpdatePasswordUserCommon(BaseModel):
    CurrentPassword: str
    NewPassword: str