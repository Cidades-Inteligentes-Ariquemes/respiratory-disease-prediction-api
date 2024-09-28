from pydantic import BaseModel


class CodeVerification(BaseModel):
    code: int
