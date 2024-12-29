from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from accounts.models import Captain
from .models import Profile
from .serializers import CaptainProfileSerializer, ClientProfileSerializer
from rest_framework.exceptions import NotFound

class CaptainProfileView(RetrieveUpdateAPIView):
    queryset = Profile.objects.filter(captain__isnull=False)  # استرجاع فقط بروفايلات الكابتن
    serializer_class = CaptainProfileSerializer
    permission_classes = [IsAuthenticated]  # تفعيل المصادقة

    def get_object(self):
        # الوصول إلى بروفايل الكابتن بناءً على العلاقة العكسية المحددة
        captain = self.request.user  # استخدام الحرف الصغير
        try:
            return captain.profile_app_captain  # استخدم related_name المناسب
        except AttributeError:
            raise NotFound("Captain profile not found")


class ClientProfileView(RetrieveUpdateAPIView):
    queryset = Profile.objects.filter(client__isnull=False)  # استرجاع فقط بروفايلات الكلاينت
    serializer_class = ClientProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        client = self.request.user
        try:
            return client.profile_app_client  # استخدم related_name المناسب
        except AttributeError:
            raise NotFound("Client profile not found")