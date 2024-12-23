from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from ..db_queries import services
import logging

logger = logging.getLogger("django")


def send_notification(user_id, message):
    print(f"Sending notification to user {user_id}")
    # created_notification_id = services.create_notification_instance(
    #     user_id, message, user_name, notification_type, profile_picture_url
    # )
    # logger.info(f"Notification created with ID: {created_notification_id}")

    # Send the notification via WebSocket
    channel_layer = get_channel_layer()
    group_name = f"user_{user_id}"  # user that will recive the notification

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "send_notification",
            "message": message,
        },
    )
