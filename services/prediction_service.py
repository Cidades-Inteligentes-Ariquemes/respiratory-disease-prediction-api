import numpy as np
from PIL import Image, UnidentifiedImageError
import os
import io
from models.model import load_model, load_model_breast_cancer
from utils.load_file import load_file_to_dictionary
from fastapi import HTTPException
import cv2


model = load_model()
model_breast_cancer = load_model_breast_cancer()

def predict_image(image_data: bytes):
    try:
        image = Image.open(io.BytesIO(image_data))

        if not image:
            raise HTTPException(status_code=400, detail="An error occurred while processing the image. Please check that the image is in the correct format and try again.")
        
        prediction = model(image)

        if not prediction[0]:
            raise HTTPException(status_code=400, detail="An error occurred while processing the image. Please check that the image is in the correct format and try again.")

        prediction[0].save_txt('results.txt')

        result_dict = load_file_to_dictionary('results.txt')
        
        if os.path.exists('results.txt'):
            os.remove('results.txt')

        return result_dict

    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="An error occurred while processing the image. Please check that the image is in the correct format and try again.")
    
    except HTTPException as http_exc:
        raise http_exc


def detect_breast_cancer(image_data: bytes):
    try:
        image = Image.open(io.BytesIO(image_data)).convert('RGB')
        image_np = np.array(image)

        if image_np.size == 0:
            raise HTTPException(status_code=400, detail="A imagem está vazia ou não pode ser processada.")

        results = model_breast_cancer(image_np)

        detections = []
        if len(results[0].boxes) > 0:
            annotated_image = results[0].plot()
            annotated_image = cv2.cvtColor(np.array(annotated_image), cv2.COLOR_RGB2BGR)
            for box in results[0].boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                xyxy = box.xyxy[0].cpu().numpy().tolist()
                detections.append({
                    "class_id": cls,
                    "confidence": conf,
                    "bbox": xyxy
                })
        else:
            annotated_image = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        success, img_encoded = cv2.imencode('.jpg', annotated_image)
        if not success:
            raise HTTPException(status_code=500, detail="Falha ao codificar a imagem.")
        img_bytes = img_encoded.tobytes()

        return {
            "image": img_bytes,
            "detections": detections
        }

    except UnidentifiedImageError:
        raise HTTPException(
            status_code=400,
            detail="Error processing the image. Please ensure the format is correct and try again."
        )
    except HTTPException as http_exc:
        raise http_exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing the image. Please try again later."
        ) from exc
