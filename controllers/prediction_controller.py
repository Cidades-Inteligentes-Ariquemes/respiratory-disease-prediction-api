from fastapi import UploadFile
from services import prediction_service

async def handle_prediction(file: UploadFile):
    image = await file.read()
    
    prediction = prediction_service.predict_image(image)
    
    return {"prediction": prediction}
