from rest_framework.views import APIView
from .db_queries import selectors, services
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .Tasks import notifications_tasks
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.request import Request
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


# class GetUserNotifications(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         Response_data, Response_status = selectors.get_user_notifications(request)
#         return Response(Response_data, Response_status)


# class MarkSpecificNotificationAsRead(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         Response_data, Response_status = services.mark_specific_notification_as_read(request)
#         return Response(Response_data, Response_status)


# class MarkAllNotificationsAsRead(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         Response_data, Response_status = services.mark_all_notifications_as_read(request)
#         return Response(Response_data, Response_status)


class SendNotificationView(APIView):
    def post(self, request: Request):
        notifications_tasks.send_notification(
            user_id=request.GET["user_id"],
            message=request.GET["message"],
        )
        # channel_layer = get_channel_layer()
        # user_id = request.GET["user_id"]
        # message = request.GET["message"]

        # async_to_sync(channel_layer.group_send)(
        #     f"user_{user_id}",
        #     {
        #         "type": "send_notification",
        #         "message": message,
        #         "notification_type": "orders",
        #         "id": "123",
        #         "user_name": "test_name",
        #         "profile_picture": "test_logo_url",
        #     },
        # )
        return Response({"status": "Notification sent"})


@csrf_exempt
def login(request):
    return render(request, "login.html")


def index(request):
    token = request.session.get("access_token", "")
    return render(request, "test_notifications.html", {"token": token})
