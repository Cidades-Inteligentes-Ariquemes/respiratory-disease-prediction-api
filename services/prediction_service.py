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
        
        # Normaliza o tamanho da imagem
        max_dimension = 1024  # Dimensão máxima permitida
        width, height = image.size
        
        # Calcula a nova dimensão mantendo a proporção
        if width > max_dimension or height > max_dimension:
            if width > height:
                new_width = max_dimension
                new_height = int((height * max_dimension) / width)
            else:
                new_height = max_dimension
                new_width = int((width * max_dimension) / height)
            
            # Redimensiona a imagem mantendo a qualidade
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
        image_np = np.array(image)

        if image_np.size == 0:
            raise HTTPException(status_code=400, detail="A imagem está vazia ou não pode ser processada.")

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

            labels_map = {1: 'Mass'}

            # Calcula dimensões mínimas garantidas para visualização
            image_width, image_height = image.size
            min_line_width = max(3, int(min(image_width, image_height) * 0.005))
            min_font_size = max(16, int(min(image_width, image_height) * 0.02))

            for box, label, score in zip(boxes, labels, scores):
                xmin, ymin, xmax, ymax = box
                xmin, ymin, xmax, ymax = int(xmin), int(ymin), int(xmax), int(ymax)

                # Calcula a largura e altura da caixa delimitadora
                box_width = xmax - xmin
                box_height = ymax - ymin

                # Define espessura da linha proporcional à imagem, com mínimo garantido
                line_width = max(min_line_width, int(min(box_width, box_height) * 0.02))

                # Define tamanho da fonte proporcional à imagem, com mínimo garantido
                font_size = max(min_font_size, int(min(box_width, box_height) * 0.1))

                try:
                    font = ImageFont.truetype("arial.ttf", size=font_size)
                except IOError:
                    # Se arial.ttf não estiver disponível, tenta DejaVuSans
                    try:
                        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size=font_size)
                    except IOError:
                        font = ImageFont.load_default()

                # Desenha a caixa delimitadora com borda dupla para maior destaque
                # Borda externa preta
                draw.rectangle([(xmin-line_width, ymin-line_width), 
                              (xmax+line_width, ymax+line_width)], 
                              outline='black', width=line_width+2)
                # Borda interna colorida
                draw.rectangle([(xmin, ymin), (xmax, ymax)], 
                             outline='red', width=line_width)

                # Obtém o nome da classe
                class_name = labels_map.get(label, 'desconhecido')

                # Cria o texto com o rótulo e a pontuação
                text = f"{score:.2f}"

                # Calcula a posição e o tamanho do texto
                text_size = draw.textbbox((0, 0), text, font=font)
                text_width = text_size[2] - text_size[0]
                text_height = text_size[3] - text_size[1]

                # Adiciona padding ao texto para melhor legibilidade
                padding = max(4, int(text_height * 0.2))

                # Coordenadas para o fundo do texto
                text_xmin = xmin
                text_ymin = max(0, ymin - text_height - padding * 2)  # Garante que não saia da imagem
                text_xmax = xmin + text_width + padding * 2
                text_ymax = text_ymin + text_height + padding * 2

                # Se o texto ficaria fora da imagem no topo, coloca abaixo da caixa
                if text_ymin < 0:
                    text_ymin = min(ymax, image_height - text_height - padding * 2)
                    text_ymax = text_ymin + text_height + padding * 2

                # Desenha um contorno preto ao redor do fundo do texto
                draw.rectangle([(text_xmin-2, text_ymin-2), (text_xmax+2, text_ymax+2)], 
                             fill='red')
                # Desenha o retângulo de fundo para o texto
                draw.rectangle([(text_xmin, text_ymin), (text_xmax, text_ymax)], 
                             fill='red')

                # Escreve o texto com contorno preto para maior contraste
                for offset in [(1,1), (-1,-1), (1,-1), (-1,1)]:
                    draw.text((text_xmin + padding + offset[0], text_ymin + padding + offset[1]),
                            text, fill='black', font=font)
                # Texto principal em branco
                draw.text((text_xmin + padding, text_ymin + padding),
                         text, fill='white', font=font)

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
        success, img_encoded = cv2.imencode('.jpg', annotated_image, [cv2.IMWRITE_JPEG_QUALITY, 95])
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
            detail="Erro ao processer a imagem. Verifique se o formato está correto e tente novamente."
        )
    except HTTPException as http_exc:
        raise http_exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Ocorreu um erro ao processar a imagem. Por favor, tente novamente mais tarde."
            ) from exc





