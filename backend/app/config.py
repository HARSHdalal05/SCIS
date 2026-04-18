from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/fitmorph"
    jwt_secret: str = "dev-secret-change-me"
    otp_bypass_code: str = "123456"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
