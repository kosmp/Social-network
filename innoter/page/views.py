import logging
from datetime import datetime, timedelta

from post.serializers import PostSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Follower, Page
from .paginations import CustomPageNumberPagination
from .permissions import (
    IsAdminOrIsModeratorOfThePageOwner,
    IsAdminOrIsOwnerOrIsModeratorOfTheOwner,
    IsAuthenticated,
    IsPageOwner,
)
from .serializers import PageSerializer
from .utils import get_user_info, upload_file

logger = logging.getLogger(__name__)


class PageViewSet(ModelViewSet):
    queryset = Page.objects.all()

    serializer_class = PageSerializer
    pagination_class = CustomPageNumberPagination

    permission_classes_by_action = {
        "create": [IsAuthenticated],
        "destroy": [IsAdminOrIsOwnerOrIsModeratorOfTheOwner],
        "retrieve": [IsAuthenticated],
        "list": [IsAuthenticated],
        "update": [IsPageOwner],
        "partial_update": [IsPageOwner],
    }

    def perform_update(self, serializer):
        key = serializer.validated_data.get("name") or self.get_object().name
        key = upload_file(key, serializer, self.request)

        serializer.save(image_url=key)

    def perform_create(self, serializer):
        logger.info("Creating page. Invoked perform_create.")
        user_data = get_user_info(self.request)
        key = upload_file(None, serializer, self.request)

        serializer.save(
            user_id=user_data.get("user_id"),
            owner_group_id=user_data.get("group_id"),
            image_url=key,
        )
        logger.info("Page successfully created.")

    def get_permissions(self):
        try:
            return [
                permission()
                for permission in self.permission_classes_by_action[self.action]
            ]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def retrieve(self, request, *args, **kwargs):
        logger.info("Retrieving page. Invoked retrieve action.")
        instance = self.get_object()
        queryset = instance.posts.all()

        posts = self.paginate_queryset(queryset)
        serializer = PostSerializer(posts, many=True)

        response = self.get_paginated_response(serializer.data)

        page_data = self.get_serializer(instance).data
        page_data.update(response.data)

        response.data = page_data
        return response

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAuthenticated],
    )
    def post(self, request, pk=None):
        logger.info("Invoked post action.")
        page = self.get_object()
        data = request.data.copy()
        data["page"] = page.id
        logger.info(f"Page id is {page.id}.")
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Post successfully saved.")
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @action(
        detail=True,
        methods=["patch"],
        permission_classes=[IsAdminOrIsModeratorOfThePageOwner],
    )
    def block(self, request, pk=None):
        logger.info("Blocking page. Invoked block action.")
        page = self.get_object()
        page.is_blocked = True
        unblock_date = request.data.get("unblock_date")
        if unblock_date:
            try:
                unblock_date = datetime.strptime(unblock_date, "%Y-%m-%d").date()
                if unblock_date < datetime.now().date():
                    return Response(
                        {"error": "Unblock date must be in the future."}, status=400
                    )
                page.unblock_date = unblock_date
            except ValueError:
                logger.error(
                    "Invalid unblock date format. Expected format: YYYY-MM-DD."
                )
                return Response(
                    {
                        "error": "Invalid unblock date format. Expected format: YYYY-MM-DD."
                    },
                    status=400,
                )
        else:
            unblock_date = datetime.now().date() + timedelta(days=30)
            page.unblock_date = unblock_date
        page.save()
        logger.info(f"Page with id {pk} successfully blocked.")
        return Response({"message": f"Page {pk} has been blocked."})

    @action(detail=True, methods=["patch"], permission_classes=[IsAuthenticated])
    def follow(self, request, pk=None):
        logger.info("Invoked follow action.")
        page = self.get_object()
        user_id = get_user_info(self.request).get("user_id")
        response = None
        if Follower.objects.follow_page(page, user_id):
            logger.info(f"User with id {user_id} followed page with id {page.id}.")
            response = Response({"message": f"You are now following page {page.id}."})
        else:
            logger.info(
                f"User with id {user_id} are already following page with id {page.id}."
            )
            response = Response(
                {"message": f"You are already following page {page.id}."}
            )
        return response

    @action(detail=True, methods=["patch"], permission_classes=[IsAuthenticated])
    def unfollow(self, request, pk=None):
        logger.info("Invoked unfollow action.")
        page = self.get_object()
        user_id = get_user_info(self.request).get("user_id")
        response = None
        if Follower.objects.unfollow_page(page, user_id):
            logger.info(f"User with id {user_id} unfollowed page with id {page.id}.")
            response = Response({"message": f"You no longer following page {page.id}."})
        else:
            logger.info(
                f"User with id {user_id} are not following page with id {page.id}."
            )
            response = Response({"message": f"You are not following page {page.id}."})
        return response

    @action(
        detail=True,
        methods=["get"],
        permission_classes=[IsAuthenticated],
    )
    def followers(self, request, pk=None):
        logger.info("Invoked get followers action.")
        page = self.get_object()
        followers = Follower.objects.filter(page=pk).values("user_id")
        return Response(followers)
