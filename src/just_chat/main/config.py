from dataclasses import dataclass
from os import getenv

RABBIT_URL_ENV = "RABBIT_URL"

MINIO_ENDPOINT_ENV = "MINIO_ENDPOINT"
MINIO_ACCESS_KEY_ENV = "MINIO_ACCESS_KEY"
MINIO_SECRET_KEY_ENV = "MINIO_SECRET_KEY"

MONGO_DSN_ENV = "MONGO_DSN"

POSTGRES_DSN_ENV = "POSTGRES_DSN"


class ConfigError(Exception):
    pass


class EnvVarNotSetError(ConfigError):
    def __init__(self, env_var_name: str) -> None:
        super().__init__(f"Environment variable {env_var_name} is not set")


@dataclass
class RabbitSettings:
    url: str


@dataclass
class MinioSettings:
    endpoint: str
    access_key: str
    secret_key: str


@dataclass
class MongoSettings:
    dsn: str


@dataclass
class PostgresSettings:
    dsn: str


def load_str_env(key: str) -> str:
    env = getenv(key)

    if env is None:
        raise EnvVarNotSetError(key)

    return env


def get_minio_settings() -> MinioSettings:
    return MinioSettings(
        endpoint=load_str_env(MINIO_ENDPOINT_ENV),
        access_key=load_str_env(MINIO_ACCESS_KEY_ENV),
        secret_key=load_str_env(MINIO_SECRET_KEY_ENV),
    )


def get_mongo_settings() -> MongoSettings:
    return MongoSettings(
        dsn=load_str_env(MONGO_DSN_ENV),
    )


def get_postgres_settings() -> PostgresSettings:
    return PostgresSettings(
        dsn=load_str_env(POSTGRES_DSN_ENV),
    )


def get_rabbit_settings() -> RabbitSettings:
    return RabbitSettings(
        url=load_str_env(RABBIT_URL_ENV),
    )
