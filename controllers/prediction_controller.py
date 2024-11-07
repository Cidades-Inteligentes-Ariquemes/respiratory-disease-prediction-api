from fastapi import UploadFile
from services import prediction_service
from fastapi.responses import JSONResponse
import base64
import io


async def handle_prediction(file: UploadFile):
    image = await file.read()
    
    prediction = prediction_service.predict_image(image)
    
    return {"prediction": prediction}

async def handle_detect_breast_cancer(file: UploadFile):
    image_data = await file.read()
    
    result = prediction_service.detect_breast_cancer(image_data)
    
    image_base64 = base64.b64encode(result["image"]).decode('utf-8')
    
    return JSONResponse(content={
        "detections": result["detections"],
        "image": image_base64
    })
