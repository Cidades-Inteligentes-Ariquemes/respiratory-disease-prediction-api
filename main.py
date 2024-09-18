from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from routes.prediction_route import router as prediction_route
from routes.user_route import router as user_route
from utils import custom_openapi

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.openapi = lambda: custom_openapi.custom_openapi(app)

app.include_router(prediction_route, tags=["prediction"])
app.include_router(user_route, tags=["user"])

@app.get("/")
def read_root():
    return {"Bem vindo a API de predição de doênças respiratórias através da imagem de raio-x que contenha o pulmão. Faça seu credenciamento e acesse a endpoint '/predict' e envie uma imagem para obter a previsão."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
