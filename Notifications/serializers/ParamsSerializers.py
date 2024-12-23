from rest_framework.serializers import (
    Serializer,
    IntegerField,
    CharField,
    ValidationError,
)
from ..models import NotificationsTypes


class NotificationIDValidator(Serializer):
    notification_id = IntegerField()


class NotificationTypeValidator(Serializer):
    notification_type = CharField()

    def validate_notification_type(self, value):
        if value not in NotificationsTypes.values:
            raise ValidationError("Invalid notification type")
        return value
