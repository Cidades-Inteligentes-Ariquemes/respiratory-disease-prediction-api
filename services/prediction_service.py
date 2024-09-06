import numpy as np
from PIL import Image
import os
import io
from models.model import load_model
from utils.load_file import load_file_to_dictionary

model = load_model()

def predict_image(image_data: bytes):
    
    try:
        image = Image.open(io.BytesIO(image_data))
   
        prediction = model(image)

        prediction[0].save_txt('results.txt')

        result_dict = load_file_to_dictionary('results.txt')
        
        if os.path.exists('results.txt'):
            os.remove('results.txt')

        return result_dict
    except Exception as e:
        print(e)
        return {"Error": "Ocorreu um erro ao processar a imagem. Verifique se a imagem está no formato correto e tente novamente."}
