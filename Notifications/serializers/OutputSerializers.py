from rest_framework.serializers import (  # noqa
    ModelSerializer,
)
from .. import models


class NotificationsSerializer(ModelSerializer):
    class Meta:
        model = models.NotificationsModel
        fields = (
            "id",
            "user_name",
            "profile_picture_url",
            "message",
            "is_read",
            "created_at",
        )
