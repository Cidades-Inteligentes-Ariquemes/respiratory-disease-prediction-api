from fastapi import APIRouter, UploadFile, File
from controllers import prediction_controller
from utils.examples_routes_returns import ResponseExamples

router = APIRouter()

response_examples = ResponseExamples()

@router.post("/predict", responses=response_examples.handle_prediction())
async def predict(file: UploadFile = File(...)):
    return await prediction_controller.handle_prediction(file)

@router.post("/detect")
async def detect_breast_cancer(file: UploadFile = File(...)):
    return await prediction_controller.handle_detect_breast_cancer_with_fastRCNN(file)
