from pathlib import Path

from pydantic_settings import BaseSettings


class PydanticSettings(BaseSettings):
    mysql_database: str = None
    mysql_user: str = None
    mysql_password: str = None
    mysql_root_password: str = None
    mysql_host: str = None
    mysql_port: int = None
    jwt_secret_key: str = None
    algorithm: str = None
    secret_key: str = None
    app_port: int = None
    celery_broker_url: str = None
    celery_result_backend: str = None
    logging_filename: str = None
    logging_to_file_enabled: str = "False"


p_settings = PydanticSettings(
    _env_file=str(Path(__file__).parent.parent.parent / ".env"),
    _env_file_encoding="utf-8",
)
