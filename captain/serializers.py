from rest_framework import serializers
from .models import CaptainProfile

class CaptainProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaptainProfile
        fields = ['license_number', 'vehicle_type', 'city', 'profile_picture']
