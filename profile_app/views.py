from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Profile
from .serializers import CaptainProfileSerializer, ClientProfileSerializer

class CaptainProfileView(RetrieveUpdateAPIView):
    queryset = Profile.objects.filter(captain__isnull=False)  # استرجاع فقط بروفايلات الكابتن
    serializer_class = CaptainProfileSerializer
    permission_classes = [IsAuthenticated]  # تفعيل المصادقة

    def get_object(self):
        # الوصول إلى بروفايل الكابتن بناءً على العلاقة العكسية المحددة
        captain = self.request.user
        if not hasattr(captain, 'profile_app_captain'):  # تأكد من وجود العلاقة العكسية
            raise Profile.DoesNotExist("Captain profile not found")
        return captain.profile_app_captain  # استخدم related_name المناسب

class ClientProfileView(RetrieveUpdateAPIView):
    queryset = Profile.objects.filter(client__isnull=False)  # استرجاع فقط بروفايلات الكلاينت
    serializer_class = ClientProfileSerializer
    permission_classes = [IsAuthenticated]  # تفعيل المصادقة

    def get_object(self):
        # الوصول إلى بروفايل الكلاينت بناءً على العلاقة العكسية المحددة
        client = self.request.user
        if not hasattr(client, 'profile_app_client'):  # تأكد من وجود العلاقة العكسية
            raise Profile.DoesNotExist("Client profile not found")
        return client.profile_app_client  # استخدم related_name المناسب
