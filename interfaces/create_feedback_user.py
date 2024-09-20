from pydantic import BaseModel


class CreateFeedbackUser(BaseModel):
    user_name: str
    feedback: str
    prediction_made: str
    correct_prediction: str
