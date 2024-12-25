from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CaptainProfile
from .serializers import CaptainProfileSerializer

class CompleteCaptainProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        profile, created = CaptainProfile.objects.get_or_create(captain_user=request.user)
        serializer = CaptainProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully!"})
        return Response(serializer.errors, status=400)
