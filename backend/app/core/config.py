import os

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    ENV: str = "development"
    DEBUG: bool = True
    WRITER_DB_URL: str = "sqlite://:memory:"  # Default is a sqlite in memory
    READER_DB_URL: str = "sqlite://:memory:"  # Default is a sqlite in memory
    JWT_SECRET_KEY: str = "fastapi"
    JWT_ALGORITHM: str = "HS256"
    SENTRY_SDN: str = 'test'
    CELERY_BROKER_URL: str = "amqp://user:bitnami@localhost:5672/"
    CELERY_BACKEND_URL: str = "redis://:password123@localhost:6379/0"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379


class DevelopmentConfig(Config):
    WRITER_DB_URL: str = "sqlite://:memory:"  # Default is a sqlite in memory
    READER_DB_URL: str = "sqlite://:memory:"  # Default is a sqlite in memory
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379


class LocalConfig(Config):
    WRITER_DB_URL: str = "sqlite://:memory:"  # Default is a sqlite in memory
    READER_DB_URL: str = "sqlite://:memory:"  # Default is a sqlite in memory


class ProductionConfig(Config):
    DEBUG: str = False
    WRITER_DB_URL: str = "sqlite://:memory:"  # Default is a sqlite in memory
    READER_DB_URL: str = "sqlite://:memory:"  # Default is a sqlite in memory


def get_config():
    env = os.getenv("ENV", "local")
    config_type = {
        "dev": DevelopmentConfig(),
        "local": LocalConfig(),
        "prod": ProductionConfig(),
    }
    return config_type[env]


config: Config = get_config()