from fastapi import UploadFile
from services import prediction_service

async def handle_prediction(file: UploadFile):
    # Lê o conteúdo da imagem
    image = await file.read()
    # Passa a imagem para o serviço de previsão
    prediction = prediction_service.predict_image(image)
    # Retorna a previsão
    return {"prediction": prediction}
