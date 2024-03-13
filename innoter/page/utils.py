import logging

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
