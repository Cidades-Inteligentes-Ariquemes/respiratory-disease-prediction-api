from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_url: str
    secret_key: str
    api_key: str

    class Config:
        env_file = ".env"