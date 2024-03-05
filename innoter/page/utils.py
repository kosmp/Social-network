import os

import jwt


def get_user_info(request):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    decoded = jwt.decode(
        token,
        os.environ.get("JWT_SECRET_KEY"),
        algorithms=[os.environ.get("ALGORITHM")],
    )
    user_data = {
        "user_id": decoded.get("user_id", None),
        "role": decoded.get("role", None),
        "group_id": decoded.get("group_id", None),
        "is_blocked": decoded.get("is_blocked", None),
        "token_type": decoded.get("token_type", None),
        "exp": decoded.get("exp", None),
    }

    return user_data
