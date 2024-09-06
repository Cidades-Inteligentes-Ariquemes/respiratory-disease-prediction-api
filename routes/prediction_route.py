from fastapi import APIRouter, UploadFile, File
from controllers import prediction_controller

router = APIRouter()

@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    return await prediction_controller.handle_prediction(file)
