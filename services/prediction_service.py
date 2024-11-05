# import numpy as np
# from PIL import Image
# import os
# import io
# from models.model import load_model
# from utils.load_file import load_file_to_dictionary
# from fastapi import HTTPException


# model = load_model()

# def predict_image(image_data: bytes):
    
#     try:
#         image = Image.open(io.BytesIO(image_data))

#         if not image:
#             raise HTTPException(status_code=400, detail="Ocorreu um erro ao processar a imagem. Verifique se a imagem está no formato correto e tente novamente.")
   
#         prediction = model(image)

#         if not prediction[0]:
#             raise HTTPException(status_code=400, detail="Ocorreu um erro ao processar a imagem. Verifique se a imagem está no formato correto e tente novamente.")

#         prediction[0].save_txt('results.txt')

#         result_dict = load_file_to_dictionary('results.txt')
        
#         if os.path.exists('results.txt'):
#             os.remove('results.txt')

#         return result_dict
#     except HTTPException as http_exc:
#         raise http_exc
import numpy as np
from PIL import Image, UnidentifiedImageError
import os
import io
from models.model import load_model
from utils.load_file import load_file_to_dictionary
from fastapi import HTTPException


model = load_model()

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
