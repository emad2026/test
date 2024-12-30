from rest_framework import serializers
from accounts.models import Client, OneTimePassword, Captain
#from accounts.utils import generate_tokens_for_user
#from accounts.utils import generate_tokens_for_user
from accounts.utils import send_reset_password_confirm
from accounts.validations import  validate_email, validate_password
from django.contrib.auth import get_user_model # type: ignore
from rest_framework_simplejwt.tokens import RefreshToken # type: ignore
from django.contrib.auth import authenticate # type: ignore
from rest_framework.exceptions import AuthenticationFailed # type: ignore
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer # type: ignore
from django.core.exceptions import ObjectDoesNotExist # type: ignore
from django.contrib.auth.hashers import check_password # type: ignore
from rest_framework.exceptions import ValidationError # type: ignore
from accounts.validations import  validate_email, validate_first_last_name, validate_password, validate_phone_number
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from phonenumber_field.serializerfields import PhoneNumberField # type: ignore

#Registration
class CaptainRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    #phone_number = PhoneNumberField(allow_null=True,allow_blank=True)

    class Meta:
        model = Captain
        fields = [
            "email",
            "first_name",
            "last_name",
            "password",
            "password2",
            "phone_number",
            "full_name",
        ]
        extra_kwargs = {
            "first_name": {
                "read_only": True
            },  # These are auto-generated from full_name
            "last_name": {
                "read_only": True,
            },  # These are auto-generated from full_name
        }
        
    def validate(self, data):
        validate_password(data['password'], data['password2'])
        validate_first_last_name(data['first_name'], data['last_name'])
        validate_phone_number(data['phone_number'])
        # Validate the email format
        validate_email(data['email'])
        return data

    def create(self, validated_data):
        password = validated_data.pop('password2')
        captain = Captain(**validated_data)
        captain.set_password(password)
        captain.save()
        return captain

class ClientRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    phone_number = PhoneNumberField(allow_null=True,allow_blank=True)

    class Meta:
        model = Client
        fields = [
            "email",
            "first_name",
            "last_name",
            "password",
            "password2",
            "phone_number",
            "full_name",
        ]
        extra_kwargs = {
            "first_name": {
                "read_only": True
            },  # These are auto-generated from full_name
            "last_name": {
                "read_only": True,
            },  # These are auto-generated from full_name
        }
 
    def validate(self, data):
        validate_email(data['email'])
        validate_password(data['password'], data['password2'])
        validate_first_last_name(data['first_name'], data['last_name'])
        validate_phone_number(data['phone_number'])
        return data

    def create(self, validated_data):
        password = validated_data.pop('password2')
        client = Client(**validated_data)  # Change from Captain to Client
        client.set_password(password)
        client.save()
        
        return client

'''

class OneTimePasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)  # Add email explicitly for validation

    class Meta:
        model = OneTimePassword
        fields = ['email', 'otp', 'created_at']  # Use correct model field names

    def create(self, validated_data):
        email = validated_data.pop('email')
        user = Captain.objects.get(email=email)  # Retrieve the user instance by email
        
        # Create OTP record
        otp = OneTimePassword.objects.create(user=user, **validated_data)
        return otp
'''

#Resend OTP
class CaptainResendOTPSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = Captain
        fields = ['email']

    def validate_email(self, value):
        """
        Ensure the email exists in the Captain model.
        """
        if not Captain.objects.filter(email=value).exists():
            raise serializers.ValidationError("No captain found with this email.")
        return value

class ClientResendOTPSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = Client
        fields = ['email']

    def validate_email(self, value):
        """
        Ensure the email exists in the Client model.
        """
        if not Client.objects.filter(email=value).exists():
            raise serializers.ValidationError("No client found with this email.")
        return value

#Reset password using OTP
class CaptainResetPasswordSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        otp = attrs.get("otp")
        password = attrs.get("password")
        password2 = attrs.get("password2")

        # Validate password strength
        validate_password(password,password2)

        # Validate OTP
        try:
            otp_instance = OneTimePassword.objects.get(otp=otp, captain__isnull=False)
        except OneTimePassword.DoesNotExist:
            raise ValidationError("Invalid OTP.")

        if otp_instance.is_expired():
            raise ValidationError("OTP has expired.")

        return {"captain": otp_instance.captain, "password": password}

    def save(self):
        captain = self.validated_data["captain"]
        password = self.validated_data["password"]

        # Set the new password
        captain.set_password(password)
        captain.save()

        send_reset_password_confirm(captain)
        # Delete the used OTP
        OneTimePassword.objects.filter(captain=captain).delete()

        return captain

class ClientResetPasswordSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        otp = attrs.get("otp")
        password = attrs.get("password")
        password2 = attrs.get("password2")

        # Validate password strength
        validate_password(password, password2)

        # Validate OTP
        try:
            otp_instance = OneTimePassword.objects.get(otp=otp, client__isnull=False)
        except OneTimePassword.DoesNotExist:
            raise ValidationError("Invalid OTP.")

        if otp_instance.is_expired():
            raise ValidationError("OTP has expired.")

        return {"client": otp_instance.client, "password": password}

    def save(self):
        client = self.validated_data["client"]
        password = self.validated_data["password"]

        # Set the new password
        client.set_password(password)
        client.save()

        send_reset_password_confirm(client)
        # Delete the used OTP
        OneTimePassword.objects.filter(client=client).delete()

        return client

#Login and Generate JWT Tokens
class CaptainLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            # Fetch the captain by email
            captain = Captain.objects.get(email=email)
        except Captain.DoesNotExist:
            raise AuthenticationFailed("Invalid credentials.")

        # Authenticate captain by verifying the password
        if not captain.check_password(password):
            raise AuthenticationFailed("Invalid credentials.")

        # Check if the captain is active
        if not captain.is_active:
            raise AuthenticationFailed("Captain account is deactivated.")

        return captain


class ClientLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            # Fetch the client by email
           client = Client.objects.get(email=email)
        except Client.DoesNotExist:
            raise AuthenticationFailed("Invalid credentials.")

        # Authenticate client by verifying the password
        if not client.check_password(password):
            raise AuthenticationFailed("Invalid credentials.")

        # Check if the client is active
        if not client.is_active:
            raise AuthenticationFailed("Client account is deactivated.")

        return client 

'''
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

def authenticate_captain(email, password):
    UserModel = Captain
    try:

        user = UserModel.objects.get(email=email)
        print(f"User found: {user}")
    except UserModel.DoesNotExist:
        print("User not found.")
        return None

    if user.check_password(password):
        print("Password matches.")
        return user
    print("Password does not match.")
    return None

class CaptainLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        captain = authenticate_captain(email=captain.email, password=password)  # Custom method
        if captain:
            if not captain.is_verified:
                raise serializers.ValidationError("Captain account is not verified.")
            return generate_tokens_for_user(captain)

        raise serializers.ValidationError("Invalid credentials for Captain.")
'''        


