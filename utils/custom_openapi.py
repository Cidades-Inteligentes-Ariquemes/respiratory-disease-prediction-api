from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI

def custom_openapi(app: FastAPI):
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
    title="Respiratory Disease Prediction - API",
    version="1.0.0",
    description=(
        "Esta API utiliza machine learning para auxiliar profissionais médicos "
        "na classificação de imagens de raio-X do tórax em quatro categorias: COVID-19, normal, pneumonia viral "
        "e pneumonia bacteriana. O modelo de machine learning foi desenvolvido para agilizar o processo de diagnóstico e "
        "melhorar a eficiência do atendimento médico.\n\n"
        "Além das predições, a API gerencia o controle de acesso dos usuários e fornece dados processados, permitindo que "
        "os clientes visualizem informações em uma aplicação web. Isso inclui a gestão de usuários, controle de permissões, "
        "e o upload de imagens para análise e predição pelo modelo."
    ),
    routes=app.routes,
)

    if "components" not in openapi_schema:
        openapi_schema["components"] = {}
    if "securitySchemes" not in openapi_schema["components"]:
        openapi_schema["components"]["securitySchemes"] = {}

    openapi_schema["components"]["securitySchemes"]["api_key"] = {
        "type": "apiKey",
        "name": "api_key",
        "in": "header",
    }
    openapi_schema["components"]["securitySchemes"]["token"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }
    openapi_schema["security"] = [
        {"api_key": []},
        {"token": []}
    ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema
