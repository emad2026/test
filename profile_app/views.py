from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ClientProfile
from .serializers import ClientProfileSerializer

class ClientProfileAPIView(APIView):
    def get(self, request):
        profiles = ClientProfile.objects.all()
        serializer = ClientProfileSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ClientProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
