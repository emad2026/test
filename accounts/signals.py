'''
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from accounts.models import DriverProfile, User

@receiver(pre_delete, sender=DriverProfile)
def delete_user_when_driver_deleted(sender, instance, **kwargs):
    user = instance.user
    user.delete() 
    '''

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import Client, ClientProfile

@receiver(post_save, sender=Client)
def create_client_profile(sender, instance, created, **kwargs):
    if created:
        ClientProfile.objects.create(client=instance)