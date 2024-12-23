# from ..serializers import OutputSerializers, ParamsSerializers
# from .. import models
# from rest_framework.request import Request
# from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST


# def get_user_notifications(request: Request) -> tuple[dict, int]:
#     params_serializers = ParamsSerializers.NotificationTypeValidator(data=request.GET)
#     if not params_serializers.is_valid():
#         return (
#             {"status": "error", "error": params_serializers.errors},
#             HTTP_400_BAD_REQUEST,
#         )

#     notification_type = params_serializers.validated_data["notification_type"]
#     user = request.user
#     notifications = models.NotificationsModel.objects.filter(
#         user=user, type=notification_type
#     ).order_by("-created_at")

#     number_of_notifications = request.GET.get("number_of_notifications", None)

#     if number_of_notifications:
#         notifications = notifications[: int(number_of_notifications)]

#     serializer = OutputSerializers.NotificationsSerializer(notifications, many=True)
#     return ({"status": "success", "data": serializer.data}, HTTP_200_OK)


# def get_notification(request: Request) -> tuple[dict, int]:
#     notification_id = request.data["notification_id"]
#     try:
#         target_notification_obj = models.NotificationsModel.objects.get(
#             id=notification_id, user=request.user
#         )
#     except models.NotificationsModel.DoesNotExist:
#         return (
#             {"status": "error", "error": "Notification not found"},
#             HTTP_400_BAD_REQUEST,
#         )
#     return ({"target_notification_obj": target_notification_obj}, HTTP_200_OK)


# def get_user_all_notifications(request: Request) -> tuple[dict, int]:
#     try:
#         target_notifications_instances = models.NotificationsModel.objects.filter(
#             user=request.user
#         )
#     except models.NotificationsModel.DoesNotExist:
#         return (
#             {"status": "error", "error": "Notification not found"},
#             HTTP_400_BAD_REQUEST,
#         )
#     return (
#         {"target_notifications_instances": target_notifications_instances},
#         HTTP_200_OK,
#     )
