import json
import string
from random import choices

import pytest
from post.models import Like
from rest_framework import status


class TestPostViewSet:
    def test_patch(self, api_client, user_headers, page, post):
        url = f"/api/v1/post/{post.id}/"
        data = {"content": "".join(choices(string.ascii_lowercase, k=5))}
        response = api_client.patch(
            url,
            data=json.dumps(data),
            content_type="application/json",
            headers=user_headers,
        )
        assert response.status_code == status.HTTP_200_OK

    def test_delete(self, api_client, user_headers, page, post):
        url = f"/api/v1/post/{post.id}/"
        response = api_client.delete(url, headers=user_headers)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_like(self, api_client, user_headers, page, post):
        url = f"/api/v1/post/{post.id}/like/"
        response = api_client.patch(url, headers=user_headers)
        assert response.status_code == status.HTTP_200_OK

    def test_remove_like(self, api_client, user_headers, page, post):
        Like.objects.like_post(post_id=post, user_id=page.user_id)

        url = f"/api/v1/post/{post.id}/remove_like/"
        response = api_client.patch(url, headers=user_headers)
        assert response.status_code == status.HTTP_200_OK
