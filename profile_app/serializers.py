from rest_framework import serializers
from .models import Profile

class CaptainProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['country_code']

class ClientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['country_code']
