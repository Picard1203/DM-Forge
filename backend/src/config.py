"""Application configuration loaded from environment variables."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings sourced from environment variables.

    Attributes:
        mongodb_url (str): MongoDB Atlas connection string.
        jwt_secret (str): Secret key for signing JWTs.
        jwt_algorithm (str): Algorithm used to sign JWTs.
        access_token_expire_minutes (int): Token lifetime in minutes.
        app_name (str): Human-readable application name.
    """

    mongodb_url: str
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 10080  # 7 days
    app_name: str = "The DM Forge"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


settings = Settings()
