import numpy as np
from PIL import Image, UnidentifiedImageError, ImageDraw, ImageFont
import os
import io
from models.model import load_model, load_model_breast_cancer, load_model_breast_cancer_with_fatRCNN
from utils.load_file import load_file_to_dictionary
from fastapi import HTTPException
import cv2
import torch
from torchvision.transforms import ToTensor
from torchvision.ops import nms



model = load_model()
model_breast_cancer = load_model_breast_cancer()

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
model_breast_cancer_faster_rcnn = load_model_breast_cancer_with_fatRCNN(device)

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


def detect_breast_cancer_with_fastRCNN(image_data: bytes):
    try:
        image = Image.open(io.BytesIO(image_data)).convert('RGB')
        image_np = np.array(image)

        if image_np.size == 0:
            raise HTTPException(status_code=400, detail="The image is empty or cannot be processed.")

        # Prepara a imagem para o modelo
        transform = ToTensor()
        img_tensor = transform(image).to(device)

        # Realiza a predição
        with torch.no_grad():
            prediction = model_breast_cancer_faster_rcnn([img_tensor])

        # Processa as predições
        boxes = prediction[0]['boxes']
        labels = prediction[0]['labels']
        scores = prediction[0]['scores']

        # Aplica limiar de confiança
        score_threshold = 0.4
        keep = scores >= score_threshold

        boxes = boxes[keep]
        labels = labels[keep]
        scores = scores[keep]

        nms_threshold = 0.4
        indices = nms(boxes, scores, nms_threshold)

        boxes = boxes[indices]
        labels = labels[indices]
        scores = scores[indices]

        boxes = boxes.cpu().numpy()
        labels = labels.cpu().numpy()
        scores = scores.cpu().numpy()

        detections = []
        if len(boxes) > 0:
            # Anota a imagem
            image_with_boxes = image.copy()
            draw = ImageDraw.Draw(image_with_boxes)

            try:
                font = ImageFont.truetype("arial.ttf", size=15)
            except IOError:
                font = ImageFont.load_default()

            labels_map = {1: 'Mass'}

            for box, label, score in zip(boxes, labels, scores):
                xmin, ymin, xmax, ymax = box
                xmin, ymin, xmax, ymax = int(xmin), int(ymin), int(xmax), int(ymax)

                # Desenha o retângulo da caixa
                draw.rectangle([(xmin, ymin), (xmax, ymax)], outline='blue', width=2)

                # Obtem o nome da classe
                class_name = labels_map.get(label, 'desconhecido')

                # Cria o texto com o label e o score
                text = f"{class_name}: {score:.2f}"

                # Calcula a posição e o tamanho do texto
                text_size = draw.textbbox((0, 0), text, font=font)
                text_width = text_size[2] - text_size[0]
                text_height = text_size[3] - text_size[1]

                # Coordenadas do fundo do texto
                text_xmin = xmin
                text_ymin = ymin - text_height - 5
                text_xmax = xmin + text_width
                text_ymax = ymin

                # Garantir que o texto não saia da imagem
                if text_ymin < 0:
                    text_ymin = ymin
                    text_ymax = ymin + text_height + 5

                # Desenha o retângulo de fundo
                draw.rectangle([(text_xmin, text_ymin), (text_xmax, text_ymax)], fill='blue')

                # Escreve o texto sobre o fundo
                draw.text((text_xmin, text_ymin), text, fill='white', font=font)

                # Adiciona a detecção à lista
                detections.append({
                    "class_id": int(label),
                    "confidence": float(score),
                    "bbox": [xmin, ymin, xmax, ymax]
                })

            # Converte a imagem anotada para formato OpenCV
            annotated_image = np.array(image_with_boxes)
            annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR)
        else:
            annotated_image = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        # Codifica a imagem em bytes
        success, img_encoded = cv2.imencode('.jpg', annotated_image)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to encode image.")
        img_bytes = img_encoded.tobytes()

        return {
            "image": img_bytes,
            "detections": detections
        }

    except UnidentifiedImageError:
        raise HTTPException(
            status_code=400,
            detail="Error processing image. Check if the format is correct and try again.."
        )
    except HTTPException as http_exc:
        raise http_exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing the image. Please try again later.."
            ) from exc
