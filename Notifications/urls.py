from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import (  # noqa
    TokenObtainPairView,
    TokenRefreshView,
)

url_for_test_socket = [
    path("test-notifications_page/", views.index, name="test_notifications"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("login/", views.login, name="login"),
    path("send_notification/", views.SendNotificationView.as_view()),
]

urlpatterns = [
    # path("get_all_notifications/", views.GetUserNotifications.as_view()),
    # path("mark_notification_as_read/", views.MarkSpecificNotificationAsRead.as_view()),
    # path("mark_all_notifications_as_read/", views.MarkAllNotificationsAsRead.as_view()),
    path("test_socket/", include(url_for_test_socket)),
]
