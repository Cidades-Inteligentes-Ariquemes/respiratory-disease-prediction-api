from pydantic import BaseModel


class IdVerification(BaseModel):
    id_verification: str
