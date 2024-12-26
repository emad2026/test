from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Profile
from .serializers import CaptainProfileSerializer, ClientProfileSerializer

class CaptainProfileView(RetrieveUpdateAPIView):
    queryset = Profile.objects.filter(captain__isnull=False)  # فقط بروفايل الكابتن
    serializer_class = CaptainProfileSerializer
    #permission_classes = [IsAuthenticated]

    def get_object(self):
        # الوصول إلى بروفايل الكابتن من خلال العلاقة المباشرة
        captain = self.request.user  # أو من خلال معرف معين
        if not hasattr(captain, 'profile'):
            raise Profile.DoesNotExist("Captain profile not found")
        return captain.profile

class ClientProfileView(RetrieveUpdateAPIView):
    queryset = Profile.objects.filter(client__isnull=False)  # فقط بروفايل الكلاينت
    serializer_class = ClientProfileSerializer
    #permission_classes = [IsAuthenticated]

    def get_object(self):
        # الوصول إلى بروفايل الكلاينت من خلال العلاقة المباشرة
        client = self.request.user  # أو من خلال معرف معين
        if not hasattr(client, 'profile_app_client_profile'):
            raise Profile.DoesNotExist("Client profile not found")
        return client.profile_app_client_profile

