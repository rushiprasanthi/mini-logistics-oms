from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "mini-logistics-oms"
    DEBUG: bool = True

    # Oracle Database configuration
    ORACLE_USER: str = "system"
    ORACLE_PASSWORD: str = "admin"
    ORACLE_HOST: str = "localhost"
    ORACLE_PORT: int = 1521
    ORACLE_SERVICE: str = "xe"

    # SQLAlchemy URL
    SQLALCHEMY_DATABASE_URI: str = None

    # JWT
    JWT_SECRET_KEY: str = "changeme-please-use-env"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        env_file = ".env"

    def __init__(self, **data):
        super().__init__(**data)
        if not self.SQLALCHEMY_DATABASE_URI:
            self.SQLALCHEMY_DATABASE_URI = (
                f"oracle+oracledb://"
                f"{self.ORACLE_USER}:{self.ORACLE_PASSWORD}"
                f"@{self.ORACLE_HOST}:{self.ORACLE_PORT}"
                f"/?service_name={self.ORACLE_SERVICE}"
            )


settings = Settings()
