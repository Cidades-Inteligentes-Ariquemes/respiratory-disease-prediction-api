from pydantic import BaseModel
import uuid


class CreateUser(BaseModel):
    full_name: str
    email: str
    profile: str
    password: str
