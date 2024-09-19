from pydantic import BaseModel


class CreateFeedbackUser(BaseModel):
    user_name: str
    feedback: str
