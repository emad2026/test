import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,Group,Permission # type: ignore
from django.utils.translation import gettext_lazy as _ # type: ignore
from rest_framework_simplejwt.tokens import RefreshToken # type: ignore
from datetime import timedelta
#from accounts.managers import UserManager
from django.utils import timezone # type: ignore
from phonenumber_field.modelfields import PhoneNumberField # type: ignore
from django.contrib.auth.models import AbstractUser # type: ignore
from django.contrib.auth import get_user_model # type: ignore
from django.db import models # type: ignore
from django.contrib.auth.models import User # type: ignore


class Captain(AbstractUser):
    # Override the default email validation to make it unique
    email = models.EmailField(unique=True)
    
    username= None
    is_verified=models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name", "last_name"]
    phone_number = PhoneNumberField(null=True, blank=True)


    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "Captain"
        verbose_name_plural = "Captains"



    # Define unique related_name for groups and permissions to resolve clashes
    groups = models.ManyToManyField(
        Group,
        related_name="captain_groups",  # Unique related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="captain_groups",  # Unique related_name
        blank=True
    )



class Client(AbstractUser):
    # Email field override to make it unique
    email = models.EmailField(unique=True)
    username = None  # Remove username field
    is_verified = models.BooleanField(default=False)  # Email verification status
    phone_number = PhoneNumberField(null=True, blank=True)  # Optional phone number field

    # Configure the username field for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    # String representation
    def __str__(self):
        return f"{self.email} - Client"
    
    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
    
    # Resolve clashes with groups and permissions related_name
    groups = models.ManyToManyField(
        Group,
        related_name="client_groups",  # Ensure unique related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="client_permissions",  # Ensure unique related_name
        blank=True
    )




class OneTimePassword(models.Model):
    otp = models.CharField(max_length=6)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Separate foreign keys for captain and client
    captain = models.ForeignKey(Captain, null=True, blank=True, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, null=True, blank=True, on_delete=models.CASCADE)

    def is_expired(self):
        expiry_time = self.created_at + timedelta(minutes=4)
        return timezone.now() > expiry_time

    def __str__(self):
        if self.captain:
            return f"{self.captain.email} - OTP code"
        elif self.client:
            return f"{self.client.email} - OTP code"
        return "OTP code"




'''
class Token(models.model):
    pass
'''
'''
class CaptainProfile(models.Model):
    user = models.OneToOneField(Captain, on_delete=models.CASCADE, related_name='driver_profile')
    license_number = models.CharField(max_length=100,blank=True, null=True)    
    
    def __str__(self):
        return f"Driver Profile for {self.user.email}"



class ClientProfile(models.Model):
    user = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='passenger_profile')
    #preferred_payment_method = models.CharField(max_length=50)
    
    def __str__(self):
        return f"Passenger Profile for {self.user.email}"
'''

from .managers import CaptainManager, ClientManager

# Assign the correct manager after importing
Captain.add_to_class('objects', CaptainManager())
Client.add_to_class('objects', ClientManager())
