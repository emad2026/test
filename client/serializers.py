from rest_framework import serializers
from .models import ClientProfile

class ClientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientProfile
        fields = ['address', 'city', 'preferred_payment_method', 'profile_picture']
