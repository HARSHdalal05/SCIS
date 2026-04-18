from pydantic_settings import BaseSettings
from pydantic import model_validator


class Settings(BaseSettings):
    app_env: str = "development"
    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/fitmorph"
    jwt_secret: str = "dev-secret-change-me"
    otp_bypass_code: str = "123456"

    @model_validator(mode="after")
    def validate_secret(self):
        if self.app_env.lower() == "production" and self.jwt_secret == "dev-secret-change-me":
            raise ValueError("JWT_SECRET must be changed for production.")
        return self

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
