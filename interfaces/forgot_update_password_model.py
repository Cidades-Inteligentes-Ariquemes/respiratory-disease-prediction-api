from pydantic import BaseModel


class ForgotUpadatePassword(BaseModel):
    id_verification: str
    new_password: str
