from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import prediction_route

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(prediction_route.router)

@app.get("/")
def read_root():
    return {"Bem vindo a API de predição de doênças respiratórias através da imagem de raio-x que contenha o pulmão. Acesse a endpoint '/predict' e envie uma imagem para obter a previsão."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
