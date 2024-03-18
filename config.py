import os

import dotenv
from pydantic_settings import BaseSettings

path_to_env = f"{os.getcwd()}/.env"

try:
    dotenv.read_dotenv(path_to_env)
except AttributeError:
    from dotenv import load_dotenv

    load_dotenv(dotenv_path=path_to_env)

DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_PORT = int(os.environ.get("DB_PORT"))

RABBITMQ_USER = os.environ.get("RABBITMQ_DEFAULT_USER")
RABBITMQ_DEFAULT_PASS = os.environ.get("RABBITMQ_DEFAULT_PASS")
RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST")
RABBITMQ_URL = f"amqp://{RABBITMQ_USER}:{RABBITMQ_DEFAULT_PASS}@{RABBITMQ_HOST}/"


class Settings(BaseSettings):
    database_url: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    rabbitmq_url: str = RABBITMQ_URL
    ROWS_LIMIT: int = 1000
    CONTRACTS_QUEUE: str = 'contracts_queue'
    RETRY_INTERVAL: int = 5
    ERROR_RETRY_INTERVAL: int = 10


settings = Settings()
