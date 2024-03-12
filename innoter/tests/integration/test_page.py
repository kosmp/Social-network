import json
import string
from random import choices

import pytest
from page.models import Follower
from rest_framework import status


class TestPageViewSet:
    def test_post(self, api_client, user_headers):
        url = "/api/v1/page/"
        data = {"name": "".join(choices(string.ascii_lowercase, k=5))}
        response = api_client.get(url, data=data, headers=user_headers)
        assert response.status_code == status.HTTP_200_OK

    def test_delete(self, api_client, user_headers, page):
        url = f"/api/v1/page/{page.id}/"
        response = api_client.delete(url, headers=user_headers)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_get(self, api_client, user_headers, page):
        url = f"/api/v1/page/{page.id}/"
        response = api_client.get(url, headers=user_headers)
        assert response.status_code == status.HTTP_200_OK

    def test_patch(self, api_client, user_headers, page):
        url = f"/api/v1/page/{page.id}/"
        data = {"description": "".join(choices(string.ascii_lowercase, k=10))}
        response = api_client.patch(
            url,
            data=json.dumps(data),
            content_type="application/json",
            headers=user_headers,
        )
        assert response.status_code == status.HTTP_200_OK

    def test_follow(self, api_client, user_headers, page):
        url = f"/api/v1/page/{page.id}/follow/"
        response = api_client.patch(url, headers=user_headers)
        assert response.status_code == status.HTTP_200_OK

    def test_unfollow(self, api_client, user_headers, page):
        Follower.objects.follow_page(page=page, user_id=page.user_id)

        url = f"/api/v1/page/{page.id}/unfollow/"
        response = api_client.patch(url, headers=user_headers)
        assert response.status_code == status.HTTP_200_OK

    def test_followers(self, api_client, user_headers, page):
        url = f"/api/v1/page/{page.id}/followers/"
        response = api_client.get(url, headers=user_headers)
        assert response.status_code == status.HTTP_200_OK

    def test_block(self, api_client, admin_headers, page):
        url = f"/api/v1/page/{page.id}/block/"
        response = api_client.patch(url, headers=admin_headers)
        assert response.status_code == status.HTTP_200_OK

    def test_post_create(self, api_client, user_headers, page):
        url = f"/api/v1/page/{page.id}/post/"
        data = {"content": "".join(choices(string.ascii_lowercase, k=5))}
        response = api_client.post(
            url,
            data=json.dumps(data),
            content_type="application/json",
            headers=user_headers,
        )
        assert response.status_code == status.HTTP_201_CREATED
