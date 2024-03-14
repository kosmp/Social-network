from pathlib import Path

from pydantic_settings import BaseSettings


class PydanticSettings(BaseSettings):
    mysql_database: str | None = None
    mysql_user: str | None = None
    mysql_password: str | None = None
    mysql_root_password: str | None = None
    mysql_host: str | None = None
    mysql_port: int | None = None
    jwt_secret_key: str | None = None
    algorithm: str | None = None
    secret_key: str | None = None
    app_port: int | None = None
    celery_broker_url: str | None = None
    celery_result_backend: str | None = None
    logging_filename: str | None = None
    logging_to_file_enabled: str | None = None
    debug: str | None = None


pydantic_config = PydanticSettings(
    _env_file=str(Path(__file__).parent.parent.parent / ".env"),
    _env_file_encoding="utf-8",
)
