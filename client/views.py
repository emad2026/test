from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ClientProfile
from .serializers import ClientProfileSerializer

class CompleteClientProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        profile, created = ClientProfile.objects.get_or_create(client_user=request.user)
        serializer = ClientProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully!"})
        return Response(serializer.errors, status=400)
