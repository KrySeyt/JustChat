from dataclasses import dataclass
from os import getenv

REDIS_HOST_ENV = "REDIS_HOST"
REDIS_PORT_ENV = "REDIS_PORT"

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
class RedisConfig:
    host: str
    port: int


@dataclass
class RabbitConfig:
    url: str


@dataclass
class MinioConfig:
    endpoint: str
    access_key: str
    secret_key: str


@dataclass
class MongoConfig:
    dsn: str


@dataclass
class PostgresConfig:
    dsn: str


def load_str_env(key: str) -> str:
    env = getenv(key)

    if env is None:
        raise EnvVarNotSetError(key)

    return env


def get_minio_settings() -> MinioConfig:
    return MinioConfig(
        endpoint=load_str_env(MINIO_ENDPOINT_ENV),
        access_key=load_str_env(MINIO_ACCESS_KEY_ENV),
        secret_key=load_str_env(MINIO_SECRET_KEY_ENV),
    )


def get_mongo_settings() -> MongoConfig:
    return MongoConfig(
        dsn=load_str_env(MONGO_DSN_ENV),
    )


def get_postgres_settings() -> PostgresConfig:
    return PostgresConfig(
        dsn=load_str_env(POSTGRES_DSN_ENV),
    )


def get_rabbit_settings() -> RabbitConfig:
    return RabbitConfig(
        url=load_str_env(RABBIT_URL_ENV),
    )


def get_redis_config() -> RedisConfig:
    return RedisConfig(
        host=load_str_env(REDIS_HOST_ENV),
        port=int(load_str_env(REDIS_PORT_ENV)),
    )
