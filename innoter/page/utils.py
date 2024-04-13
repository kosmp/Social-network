import hashlib
import logging

import boto3
import jwt
from jwt import InvalidTokenError

from innoter.config import pydantic_config

logger = logging.getLogger(__name__)


def get_user_info(request):
    logger.info("Invoked get_user_info to get user info from token.")
    try:
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        decoded = jwt.decode(
            token,
            pydantic_config.jwt_secret_key,
            algorithms=[pydantic_config.algorithm],
        )
        user_data = {
            "user_id": decoded.get("user_id"),
            "role": decoded.get("role"),
            "group_id": decoded.get("group_id"),
            "is_blocked": decoded.get("is_blocked"),
            "token_type": decoded.get("token_type"),
            "exp": decoded.get("exp"),
        }

        return user_data
    except (InvalidTokenError, jwt.ExpiredSignatureError) as err:
        logger.error(
            f"Error occurred while getting user info from token. Error: {err}."
        )
        return {}


def upload_file(key, serializer, request):
    file = request.FILES.get("image")
    if file:
        key = serializer.validated_data.get("name") or key
        raw_data = file.read()

        image_hash = hashlib.md5()
        image_hash.update(raw_data)
        image_hash.update(key.encode())

        combined_hash = image_hash.hexdigest()

        filename = f"{combined_hash}.png"
        upload_file_s3(raw_data, filename)

        return f"{pydantic_config.localstack_endpoint_url}/{pydantic_config.bucket_name}/{filename}"
    else:
        return None


session = boto3.Session(
    aws_access_key_id=pydantic_config.localstack_access_key_id,
    aws_secret_access_key=pydantic_config.localstack_secret_access_key,
)

s3 = session.client(
    "s3",
    endpoint_url=pydantic_config.localstack_endpoint_url,
    region_name="eu-central-1",
)


def upload_file_s3(file, key):
    s3.put_object(Body=file, Bucket=pydantic_config.bucket_name, Key=key)
