import json
import string
from random import choices

import pytest
from rest_framework import status


class TestTagViewSet:
    def test_post(self, api_client, user_headers):
        url = "/api/v1/tag/tag/"
        data = {"name": "".join(choices(string.ascii_lowercase, k=5))}
        response = api_client.post(
            url,
            data=json.dumps(data),
            content_type="application/json",
            headers=user_headers,
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_get(self, api_client, user_headers, tag, page):
        url = f"/api/v1/tag/tags/?filter_by_name={tag.name}/"
        response = api_client.get(url, headers=user_headers)
        assert response.status_code == status.HTTP_200_OK
