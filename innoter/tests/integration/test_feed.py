import pytest
from rest_framework import status


@pytest.mark.django_db
class TestFeedViewSet:
    def test_get(self, api_client, user_headers, setup_feed):
        url = "/api/v1/feed/"
        response = api_client.get(url, headers=user_headers)
        assert response.status_code == status.HTTP_200_OK
