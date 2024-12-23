# from rest_framework.request import Request
# from ..serializers import ParamsSerializers
# from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
# from typing import Any
# from . import selectors
# from .. import models
# # from apps.Users.models import User


# def mark_specific_notification_as_read(request: Request) -> tuple[dict[str, Any], int]:
#     params_serialzer = ParamsSerializers.NotificationIDValidator(data=request.data)
#     if not params_serialzer.is_valid():
#         return (
#             {"status": "error", "error": params_serialzer.errors},
#             HTTP_400_BAD_REQUEST,
#         )

#     response_data, response_status = selectors.get_notification(request)
#     if response_status == HTTP_400_BAD_REQUEST:
#         return response_data, response_status

#     target_notification = response_data["target_notification_obj"]

#     target_notification.is_read = True
#     target_notification.save()
#     return ({"status": "success"}, HTTP_200_OK)


# def mark_all_notifications_as_read(request: Request) -> tuple[dict[str, Any], int]:
#     response_data, response_status = selectors.get_user_all_notifications(request)
#     if response_status == HTTP_400_BAD_REQUEST:
#         return response_data, response_status
#     target_notifications_instances = response_data["target_notifications_instances"]
#     target_notifications_instances.update(is_read=True)

#     return ({"status": "success"}, HTTP_200_OK)


# def create_notification_instance(
#     user_id: int,
#     message: str,
#     user_name: str,
#     notification_type: str,
#     profile_picture_url: str,
# ):

#     user = User.objects.get(id=user_id)
#     created_notification = models.NotificationsModel.objects.create(
#         user=user,
#         message=message,
#         user_name=user_name,
#         type=notification_type,
#         profile_picture_url=profile_picture_url,
#     )
#     return created_notification.id
