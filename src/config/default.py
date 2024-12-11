from pathlib import Path

from fastapi.security import OAuth2PasswordBearer
from fastapi_mail import ConnectionConfig
from pydantic import PostgresDsn, SecretStr
from passlib.context import CryptContext
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_TITLE: str = "Clienthub"
    APP_DESCRIPTION: str = "API clienthub"
    APP_VERSION: str = "0.1.0"

    PATH_PREFIX: str = "/api/v1"
    APP_HOST: str = "http://0.0.0.0"
    APP_PORT: int = 8000

    POSTGRES_HOST: str = "db"
    POSTGRES_USER: str = "test"
    POSTGRES_PORT: int = 5432
    POSTGRES_PASSWORD: str = "hackme"
    POSTGRES_DB: str = "db"

    SECRET_KEY: SecretStr = (
        "unsecured2*t@t3b#6g$^w@zsdz57^x-g^o05@e5aztfn=)r#ijaly1-cy0"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    ALGORITHM: str = "HS256"
    PWD_CONTEXT: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
    OAUTH2_SCHEME: OAuth2PasswordBearer = OAuth2PasswordBearer(
        tokenUrl=f"/api/v1/user/authentication"
    )

    MAIL_USERNAME: str = "deniska_maltsev_04@mail.ru"
    MAIL_PASSWORD: str = "wbf0CmiVNzGALuBwtVy0"
    MAIL_FROM: str = "deniska_maltsev_04@mail.ru"
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.mail.ru"
    MAIL_FROM_NAME: str = "Desired Name"
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    MAIL_USE_CREDENTIALS: bool = True
    MAIL_VALIDATE_CERTS: bool = True

    ALLOW_ORIGINS: list[str] = ["*"]
    ALLOW_HOSTS: list[str] = ["*"]

    YOOKASSA_ACCOUNT_ID: str = "993185"
    YOOKASSA_SECRET_KEY: str = "test_F4i-zNB2XvgXrBN5XAJ1orEOw66bidJ9fHyuhNNCqqw"
    AMOUNT: int = 1
    REDIRECT_URL: str = "http://0.0.0.0:8000/api/swagger"

    @property
    def database_url_async(self) -> PostgresDsn:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"  # noqa

    @property
    def database_url_sync(self) -> PostgresDsn:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"  # noqa

    @property
    def mail_connect_config(self):
        return ConnectionConfig(
            MAIL_USERNAME=self.MAIL_USERNAME,
            MAIL_PASSWORD=self.MAIL_PASSWORD,
            MAIL_FROM=self.MAIL_FROM,
            MAIL_PORT=self.MAIL_PORT,
            MAIL_SERVER=self.MAIL_SERVER,
            MAIL_FROM_NAME=self.MAIL_FROM_NAME,
            MAIL_STARTTLS=self.MAIL_STARTTLS,
            MAIL_SSL_TLS=self.MAIL_SSL_TLS,
            USE_CREDENTIALS=self.MAIL_USE_CREDENTIALS,
            VALIDATE_CERTS=self.MAIL_VALIDATE_CERTS,
        )

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parents[1] / ".env", extra="ignore"
    )
