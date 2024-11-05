from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_url: str
    server: str
    port: int
    database: str
    user_pronto: str
    password: str
    secret_key: str
    api_key: str
    EMAIL: str
    EMAIL_PASSWORD: str
    APP_NAME: str

    class Config:
        env_file = ".env"